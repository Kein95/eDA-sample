// eDA 2026 enrolment capture. Writes one row to eda_registration via the
// service-role key and sends the applicant a short acknowledgement when a
// Resend key is configured.
//
// Modelled on IAIO's iaio-interest, with two deliberate differences:
//   * no dedupe — see the comment in 0001_eda_registration.sql
//   * many more fields, including guardian contact details for minors
//
// CO Y khong dung CAPTCHA. Chong bot o day dua vao honeypot (truong an) va gioi han
// tan suat theo IP ben duoi. Danh doi: mot bot chiu kho van gui duoc don rac, nhung
// doi lai khong co them dich vu ben thu ba, khong co bien moi truong nao co the bi
// xoa nham lam bao ve tat am tham, va khong co man kiem tra chan nguoi that dang ky.
import { createClient } from 'jsr:@supabase/supabase-js@2';

// Chi nhan don tu chinh trang tuyen sinh. Truoc day de "*", tuc bat ky website nao
// cung goi thang duoc endpoint nay bang trinh duyet cua khach - de bi nhung vao trang
// khac de bom don rac. Khai EDA_ALLOWED_ORIGINS dang danh sach ngan cach bang dau phay.
// Bo trong thi tro ve "*" de chay thu o localhost khong bi chan.
const ALLOWED = (Deno.env.get('EDA_ALLOWED_ORIGINS') ?? '')
  .split(',').map((s) => s.trim()).filter(Boolean);

function corsFor(req: Request): Record<string, string> {
  const origin = req.headers.get('origin') ?? '';
  const ok = ALLOWED.length === 0 ? '*' : (ALLOWED.includes(origin) ? origin : '');
  const h: Record<string, string> = {
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Vary': 'Origin',
  };
  if (ok) h['Access-Control-Allow-Origin'] = ok;
  return h;
}

const json = (body: unknown, status = 200, cors: Record<string, string> = {}) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, 'Content-Type': 'application/json' } });

// Ma giu cho phai do SERVER sinh. Truoc day client tu sinh roi gui len va server ghi
// nguyen xi, nen ai cung dat duoc ma trung hoac ma tuy y - nguoi phu trach tra cuu
// theo ma se nhin nham don. crypto.getRandomValues thay cho Math.random.
const CHU = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';   // bo I O 0 1 cho de doc qua dien thoai
function sinhMa(): string {
  const b = new Uint8Array(6);
  crypto.getRandomValues(b);
  return 'eDA26-' + [...b].map((x) => CHU[x % CHU.length]).join('');
}

const isEmail = (v: string) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
const isPhone = (v: string) => /^0\d{8,10}$/.test(v.replace(/[\s.]/g, ''));

// Trim and cap every free-text field so a bot cannot push megabytes into the table.
const clean = (v: unknown, max = 300) => String(v ?? '').trim().slice(0, max) || null;

async function ack(email: string, name: string, code: string) {
  const key = Deno.env.get('RESEND_API_KEY');
  if (!key) return;
  const from = Deno.env.get('EDA_EMAIL_FROM') ?? 'AI VIETNAM · eDA 2026 <no-reply@aivietnam.edu.vn>';
  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from, to: [email],
      subject: `eDA 2026: đã nhận đăng ký giữ chỗ (${code})`,
      html: `<p>Chào ${name},</p>
        <p>AI VIETNAM đã nhận đăng ký giữ chỗ khoá <strong>End2End Data Analytics 2026</strong>.
        Mã giữ chỗ của bạn là <strong>${code}</strong>.</p>
        <p>Đội ngũ tư vấn sẽ liên hệ trong 24 giờ làm việc. Cần trao đổi sớm hơn,
        bạn nhắn Zalo <a href="https://zalo.me/0911118758">0911 118 758</a>.</p>
        <p>Thân mến,<br />AI VIETNAM</p>`,
    }),
  }).catch(() => {});
}

// Bam IP kem mot chuoi bi mat. Luu IP tho la luu du lieu ca nhan them mot lan nua,
// ma de dem tan suat thi chi can biet "cung mot nguoi hay khong".
async function bamIp(ip: string | null): Promise<string | null> {
  if (!ip) return null;
  const muoi = Deno.env.get('EDA_IP_SALT') ?? Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '';
  const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(muoi + '|' + ip));
  return [...new Uint8Array(d)].slice(0, 16).map((x) => x.toString(16).padStart(2, '0')).join('');
}

Deno.serve(async (req) => {
  const cors = corsFor(req);
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  // Origin la trong danh sach thi moi tra header CORS; thieu header thi trinh duyet
  // tu chan. Chan luon o day cho ro rang thay vi de trinh duyet tu xu ly.
  if (ALLOWED.length && !cors['Access-Control-Allow-Origin']) return json({ error: 'origin_not_allowed' }, 403);
  if (req.method !== 'POST') return json({ error: 'method_not_allowed' }, 405, cors);

  let b: Record<string, unknown>;
  try { b = await req.json(); } catch { return json({ error: 'bad_json' }, 400, cors); }

  // Honeypot: a field hidden from humans by CSS. Anything filling it is scripted.
  // Answer 200 so the bot cannot tell it was rejected.
  if (clean(b.website)) return json({ status: 'received' }, 200, cors);

  const ip = (req.headers.get('x-forwarded-for') || '').split(',')[0].trim() || null;

  const name = clean(b.name, 120);
  const phone = clean(b.phone, 30);
  const email = (clean(b.email, 160) ?? '').toLowerCase();
  if (!name) return json({ error: 'invalid_name' }, 400, cors);
  if (!phone || !isPhone(phone)) return json({ error: 'invalid_phone' }, 400, cors);
  if (!email || !isEmail(email)) return json({ error: 'invalid_email' }, 400, cors);
  const code = sinhMa();

  const admin = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);

  // Gioi han tan suat theo IP: mot mang may khong the bom hang nghin don rac trong
  // dem, vua lam ban bang vua ton tien du an. Nguong rong tay vi ca nha co the dang
  // ky cho nhieu con tu cung mot mang.
  const ipHash = await bamIp(ip);
  const NGUONG = Number(Deno.env.get('EDA_MAX_PER_HOUR') ?? '10');
  if (ipHash) {
    const tu = new Date(Date.now() - 3600_000).toISOString();
    const { count } = await admin.from('eda_registration')
      .select('id', { count: 'exact', head: true })
      .eq('ip_hash', ipHash).gte('created_at', tu);
    if ((count ?? 0) >= NGUONG) return json({ error: 'rate_limited' }, 429, cors);
  }

  const { error } = await admin.from('eda_registration').insert({
    code, name, phone, email, ip_hash: ipHash,
    province:       clean(b.province, 80),
    job:            clean(b.job, 60),
    field:          clean(b.field, 160),
    interest:       clean(b.interest, 60),
    guardian_name:  clean(b.guardianName, 120),
    guardian_phone: clean(b.guardianPhone, 30),
    facebook:       clean(b.facebook, 200),
    zalo:           clean(b.zalo, 200),
    channel:        clean(b.channel, 80),
    note:           clean(b.note, 2000),
    user_agent:     clean(req.headers.get('user-agent'), 300),
  });
  // The applicant must not be told "saved" when it was not — the whole point of
  // this endpoint is that submissions stop being lost.
  if (error) return json({ error: 'server_error' }, 500, cors);

  await ack(email, name, code);
  return json({ status: 'received', code }, 200, cors);
});

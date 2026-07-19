// Kiem tra cac choi bao mat vua them. Khong dung framework, chay bang:
//   node scripts/test-bao-mat.mjs
// That bai thi thoat khac 0.
import { readFileSync } from 'node:fs';
import { webcrypto as crypto } from 'node:crypto';
import assert from 'node:assert/strict';

const goc = new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const doc = (p) => readFileSync(goc + p, 'utf8');
let so = 0;
const test = (ten, fn) => { fn(); so++; console.log('  ok  ' + ten); };

// ── 1. Ma giu cho phai do server sinh, bang nguon ngau nhien mat ma ─────────
const CHU = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
const sinhMa = () => {
  const b = new Uint8Array(6);
  crypto.getRandomValues(b);
  return 'eDA26-' + [...b].map((x) => CHU[x % CHU.length]).join('');
};

test('ma giu cho dung dinh dang eDA26-XXXXXX', () => {
  for (let i = 0; i < 200; i++) assert.match(sinhMa(), /^eDA26-[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{6}$/);
});

test('ma khong chua ky tu de doc nham (I, O, 0, 1)', () => {
  assert.equal(/[IO01]/.test(CHU), false);
});

test('1000 ma khong trung nhau', () => {
  const s = new Set();
  for (let i = 0; i < 1000; i++) s.add(sinhMa());
  assert.equal(s.size, 1000);
});

test('client khong con tu sinh ma', () => {
  const s = doc('TuyenSinh-eDA2026.dc.html');
  assert.equal(/eDA26-'\s*\+\s*Array/.test(s), false, 'client van tu sinh ma');
  assert.ok(/\(await res\.json\(\)\)\.code/.test(s), 'client khong lay ma tu phan hoi server');
});

// ── 2. CSV: o do nguoi dang ky go khong duoc thanh cong thuc Excel ──────────
const cell = (v) => {
  let s = String(v ?? '');
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;
  return '"' + s.replace(/"/g, '""') + '"';
};

test('cell() vo hieu hoa cong thuc Excel', () => {
  for (const doc of ['=1+1', '+1', '-1', '@SUM(A1)', '=HYPERLINK("http://x","a")', '\tx', '\rx'])
    assert.ok(cell(doc).startsWith('"\''), 'chua chan: ' + JSON.stringify(doc));
});

test('cell() khong dong cham van ban binh thuong', () => {
  assert.equal(cell('Nguyễn Văn A'), '"Nguyễn Văn A"');
  assert.equal(cell('0911118758'), '"0911118758"');
  assert.equal(cell(null), '""');
});

test('cell() van thoat dau nhay kep', () => {
  assert.equal(cell('nói "xin chào"'), '"nói ""xin chào"""');
});

// ── 3. CORS chi nhan ten mien trong danh sach ──────────────────────────────
const corsFor = (origin, danhSach) => {
  const ALLOWED = danhSach.split(',').map((s) => s.trim()).filter(Boolean);
  return ALLOWED.length === 0 ? '*' : (ALLOWED.includes(origin) ? origin : '');
};

test('CORS chan ten mien la', () => {
  const ds = 'https://aivietnam.edu.vn,https://www.aivietnam.edu.vn';
  assert.equal(corsFor('https://aivietnam.edu.vn', ds), 'https://aivietnam.edu.vn');
  assert.equal(corsFor('https://ke-gian.example', ds), '');
  assert.equal(corsFor('', ds), '');
});

test('CORS de trong danh sach thi mo, de chay thu localhost', () => {
  assert.equal(corsFor('http://localhost:8791', ''), '*');
});

// ── 4. Trang admin phai ghim phien ban + SRI, va co CSP ────────────────────
test('admin.html ghim phien ban supabase-js va co SRI', () => {
  const s = doc('admin.html');
  assert.ok(/supabase-js@\d+\.\d+\.\d+\//.test(s), 'con dung phien ban tha noi (@2)');
  assert.ok(/integrity="sha384-[A-Za-z0-9+/=]{40,}"/.test(s), 'thieu integrity');
  assert.ok(/crossorigin="anonymous"/.test(s), 'thieu crossorigin, SRI se khong hieu luc');
});

test('admin.html co CSP chan script la', () => {
  const s = doc('admin.html');
  assert.ok(/Content-Security-Policy/.test(s), 'thieu CSP');
  assert.ok(/default-src 'none'/.test(s), 'CSP khong mac dinh chan');
  assert.ok(/frame-ancestors 'none'/.test(s), 'thieu frame-ancestors, co the bi nhung de clickjack');
});

// ── 5. RLS: bang dang ky khong duoc mo cho anon ────────────────────────────
test('migration khong cap quyen doc cho anon', () => {
  const m = doc('supabase/migrations/0002_eda_registration_admin_read.sql');
  assert.ok(/for select to authenticated/.test(m), 'policy khong gioi han o authenticated');
  assert.ok(/app_metadata.*EDA_ADMIN/s.test(m), 'policy khong kiem tra app_metadata role');
  assert.equal(/to anon/.test(m), false, 'co cap quyen cho anon');
});

test('bang bat RLS', () => {
  assert.ok(/enable row level security/.test(doc('supabase/migrations/0001_eda_registration.sql')));
});

test('IP luu dang bam, khong luu tho', () => {
  const m = doc('supabase/migrations/0004_eda_rate_limit_and_retention.sql');
  assert.ok(/ip_hash/.test(m), 'thieu cot ip_hash');
  assert.equal(/add column if not exists ip\b/.test(m), false, 'dang luu IP tho');
});

console.log('\n' + so + ' kiem tra deu dat.');

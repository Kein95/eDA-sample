// Dung thu muc chua DUNG nhung file can phuc vu qua web, roi deploy tu do.
//
// Vi sao can: "wrangler pages deploy ." day len TAT CA moi thu trong thu muc. No
// khong doc .gitignore, cung khong doc .assetsignore (da thu, khong an). Deploy
// thang tu goc repo la toan bo migration SQL, thu muc .git va tai lieu noi bo deu
// thanh URL cong khai.
//
//   node scripts/dung-thu-muc-xuat-ban.mjs
//   npx wrangler pages deploy .xuat-ban --project-name eda --branch master
import { rmSync, mkdirSync, cpSync, existsSync, readdirSync, statSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';

const GOC = new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const RA = join(GOC, '.xuat-ban');

// Chi nhung thu trang thuc su nap. Kiem lai bang:
//   grep -o "assets/[A-Za-z0-9._-]*" TuyenSinh-eDA2026.dc.html | sort -u
const FILE = [
  'TuyenSinh-eDA2026.dc.html',   // trang tuyen sinh
  'admin.html',                  // trang quan tri (RLS chan du lieu, khong phai chan URL)
  'support.js',                  // runtime DesignCombo
  'image-slot.js',               // web component khung anh
  'globe.html',                  // nhung bang iframe
  '_redirects',                  // dinh tuyen tab tren Pages
  '_headers',                    // frame-ancestors cho /admin (the meta khong an)
  // Logic doi soat, admin.html import truc tiep. GIU NGUYEN duong dan trong repo thay
  // vi chep ra goc: edge function eda-doi-soat cung import dung file nay, mot ban duy
  // nhat cho ca ba noi (edge function, trang demo, test).
  'supabase/functions/_shared/doi-soat.js',
  'supabase/functions/_shared/doc-sao-ke.js',

  // Trang tuyen sinh co the "eDA 2026 - Syllabus day du" tro toi day. Thieu file thi
  // link tra 404 tren ban live ma o may van chay, vi nginx xem thu phuc vu ca repo.
  'docs/eDA-2026-Syllabus.html',

  'assets/logo-full.png',
  'assets/logo-mark.png',
  'assets/dongson-drum.svg',
];
const THUMUC = [
  'assets/video',                // thumbnail video, duong dan ghep dong
];
// Anh mentor: chi ban da cat, khong day anh goc len web.
const ANH_MENTOR = /^crop-.*\.jpg$/;

rmSync(RA, { recursive: true, force: true });
mkdirSync(RA, { recursive: true });

let n = 0;
for (const f of FILE) {
  const nguon = join(GOC, f);
  if (!existsSync(nguon)) { console.log('THIEU: ' + f); continue; }
  mkdirSync(dirname(join(RA, f)), { recursive: true });
  cpSync(nguon, join(RA, f));
  n++;
}
for (const d of THUMUC) {
  if (!existsSync(join(GOC, d))) { console.log('THIEU: ' + d); continue; }
  cpSync(join(GOC, d), join(RA, d), { recursive: true });
  n += readdirSync(join(GOC, d)).length;
}
// Trinh duyet TU DONG doi /favicon.ico truoc khi doc xong <head>. Trang tuyen sinh co
// khai bao <link rel="icon"> nhung the do nam trong <helmet>, ma support.js chi chuyen no
// vao <head> luc chay - tuc la sau khi yeu cau /favicon.ico da bay di roi. Ket qua la moi
// lan tai trang deu co mot loi 404 trong console. Phuc vu luon file do la het.
cpSync(join(GOC, 'assets/logo-mark.png'), join(RA, 'favicon.ico'));
n++;

mkdirSync(join(RA, 'ava'), { recursive: true });
for (const f of readdirSync(join(GOC, 'ava'))) {
  if (!ANH_MENTOR.test(f)) continue;
  cpSync(join(GOC, 'ava', f), join(RA, 'ava', f));
  n++;
}

// Kiem: moi thu HAI trang nap phai co mat trong thu muc xuat ban.
//
// Da hai lan suyt day len ban thieu file: trang nap module bang <script type="module">
// nen thieu mot file la CA trang chet, khong phai mat mot tinh nang. Danh sach FILE o
// tren la thu cong nen se con quen nua - de may doi chieu thay vi tin tri nho.
//
// Phai soi CA HAI trang va ca ba kieu tham chieu. Ban truoc chi soi admin.html va chi bat
// "from '...'", nen no bo lot dung mot link that: the "Syllabus day du" tro toi
// docs/eDA-2026-Syllabus.html khong duoc chep, tra 404 tren live suot ma bo canh van bao
// xanh. Bo canh phu mot nua roi bao xanh con nguy hiem hon la khong co bo canh.
const THAM_CHIEU = [
  // import ... from '...'   (module cua admin.html)
  /from\s+'(\.?\/[^']+)'/g,
  // <script src="...">, <link href="...">, <a href="..."> tro toi file trong repo
  /\b(?:src|href)="(?!https?:|data:|mailto:|tel:|#|\/\/)([^"#?]+)"/g,
];
// Bo qua thu khong phai file trong repo:
//   {{ ... }}  bieu thuc DesignCombo, dia chi chi co luc chay
//   khong co duoi  duong dan tab (/dashboard, /pathway) do _redirects lo, khong phai file
const boQua = (p) =>
  !p || p.startsWith('..') || /^[A-Za-z]+:/.test(p) || p.includes('{{') || !/\.[a-z0-9]+$/i.test(p);
const canCo = new Map();      // duong dan -> trang nao tham chieu, de bao loi cho ro
for (const trang of ['admin.html', 'TuyenSinh-eDA2026.dc.html']) {
  const nguon = readFileSync(join(GOC, trang), 'utf8');
  let thay = 0;
  for (const re of THAM_CHIEU)
    for (const m of nguon.matchAll(re)) {
      thay++;
      const p = m[1].replace(/^\.?\//, '');
      if (!boQua(p)) canCo.set(p, trang);
    }
  if (!thay) {
    console.log(`KHONG THAY tham chieu nao trong ${trang} - bo canh nay da hong, sua regex.`);
    process.exit(1);
  }
}
const thieu = [...canCo].filter(([p]) => !existsSync(join(RA, p)));
if (thieu.length) {
  console.log('THIEU trong ban xuat ban (trang co tro toi nhung khong duoc chep):');
  thieu.forEach(([p, trang]) => console.log(`  ${p}   <- ${trang}`));
  console.log('Them vao mang FILE trong scripts/dung-thu-muc-xuat-ban.mjs');
  process.exit(1);
}

const dem = (d) => readdirSync(d, { withFileTypes: true })
  .reduce((t, e) => t + (e.isDirectory() ? dem(join(d, e.name)) : statSync(join(d, e.name)).size), 0);
console.log(`da dung ${RA}: ${n} file, ${(dem(RA) / 1024 / 1024).toFixed(1)} MB`);

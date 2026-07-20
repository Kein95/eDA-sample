// Dung thu muc chua DUNG nhung file can phuc vu qua web, roi deploy tu do.
//
// Vi sao can: "wrangler pages deploy ." day len TAT CA moi thu trong thu muc. No
// khong doc .gitignore, cung khong doc .assetsignore (da thu, khong an). Deploy
// thang tu goc repo la data/eDA_v9.xlsx, toan bo migration SQL va tai lieu PDF deu
// thanh URL cong khai.
//
//   node scripts/dung-thu-muc-xuat-ban.mjs
//   npx wrangler pages deploy .xuat-ban --project-name eda --branch master
import { rmSync, mkdirSync, cpSync, existsSync, readdirSync, statSync } from 'node:fs';
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
mkdirSync(join(RA, 'ava'), { recursive: true });
for (const f of readdirSync(join(GOC, 'ava'))) {
  if (!ANH_MENTOR.test(f)) continue;
  cpSync(join(GOC, 'ava', f), join(RA, 'ava', f));
  n++;
}

const dem = (d) => readdirSync(d, { withFileTypes: true })
  .reduce((t, e) => t + (e.isDirectory() ? dem(join(d, e.name)) : statSync(join(d, e.name)).size), 0);
console.log(`da dung ${RA}: ${n} file, ${(dem(RA) / 1024 / 1024).toFixed(1)} MB`);

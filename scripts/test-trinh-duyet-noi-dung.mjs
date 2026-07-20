// Kiem: sua duoc MOI chu tren trang tuyen sinh, va sua xong khong sot cho nao.
//
// Cho de sai nhat khong phai la viec thay chu, ma la PHAM VI: trang co hon 600 chuoi, ngay
// khai giang nam o 12 cau khac nhau, va co ca "8" lan "AI" lam chuoi rieng. Nen bo kiem
// nay dem tren TOAN BO DOM qua tat ca cac tab chu khong nhin mot cho.
import { mo, cho, boDem, goc } from './lib-trinh-duyet.mjs';

const G = goc();
const d = boDem();
const MOI = 'CHU MOI KIEM THU TAB SAU';

// 1. Trang quan tri quet chu
const q = await mo(G, '/dashboard');
await q.doi(`typeof LA_DASHBOARD !== 'undefined'`);
await q.js(`['eda-noi-dung','eda-noi-dung-nhap','eda-noi-dung-goc'].forEach(k=>localStorage.removeItem(k))`);
await q.js(`location.reload()`);
await cho(1500);
await q.doi(`typeof gocTheoTab !== 'undefined'`);
await q.js(`document.querySelector('[data-tab=noidung]').click()`);
if (!await q.doi(`gocTheoTab.length`, 60)) {
  console.error('Khong quet duoc chu tren trang tuyen sinh sau 60 giay.');
  process.exit(1);
}

d.nhom('Quet chu tren trang tuyen sinh');
const tong = await q.js(`gocTheoTab.reduce((t,g)=>t+g.chuoi.length,0)`);
const soTab = await q.js(`gocTheoTab.length`);
console.log('   ', JSON.stringify(await q.js(`gocTheoTab.map(g=>g.ten+':'+g.chuoi.length)`)));
d.dat(tong > 500, `quet duoc ${tong} chuoi`);
d.dat(soTab >= 5, `gom theo ${soTab} tab`);
d.dat((await q.js(`document.querySelectorAll('#dongNoiDung textarea[data-khoa]').length`)) === tong + 4,
  `ve du o sua (${tong} chuoi + 4 bien)`);
// Khoi CSS trong <svg> co ten the viet THUONG nen tung lot vao danh sach sua duoc.
d.dat((await q.js(`gocTheoTab.some(g=>g.chuoi.some(s=>s.includes('@keyframes')))`)) === false,
  'CSS trong svg KHONG lot vao danh sach sua duoc');

await q.js(`o('timChu').value='giảng viên'; locChu()`);
const conLai = await q.js(
  `[...document.querySelectorAll('#dongNoiDung tr')].filter(t=>!t.classList.contains('hide')&&!t.classList.contains('nhomND')).length`);
d.dat(conLai > 0 && conLai < tong, `loc "giảng viên" con ${conLai}/${tong} dong`);
await q.js(`o('timChu').value=''; locChu()`);

// 2. Sua mot chuoi o tab sau, mot bien, va mot chuoi co the HTML
const chonChu = await q.js(`(()=>{
  const g = gocTheoTab.find(g=>/Tài liệu/.test(g.ten)) || gocTheoTab[gocTheoTab.length-1];
  return g.chuoi.filter(s=>s.length>15)[0];
})()`);
d.nhom(`Sua thu (chuoi o tab sau: ${JSON.stringify(chonChu)})`);
await q.js(`(()=>{
  const o = [...document.querySelectorAll('#dongNoiDung textarea[data-khoa]')];
  o.find(i=>i.dataset.khoa === 'chu:' + ${JSON.stringify(chonChu)}).value = ${JSON.stringify(MOI)};
  o.find(i=>i.dataset.khoa === 'bien:khai_giang').value = '15.10.2026';
  o.find(i=>i.dataset.khoa === 'bien:hero_tieu_de').value = '<b>Chữ mới</b> nhé';
})(); document.getElementById('xuatBan').click()`);
await cho(400);
const daXuat = JSON.parse(await q.js(`localStorage.getItem('eda-noi-dung')`));
// <input> la o MOT DONG nen nuot ky tu xuong dong: chuoi nhieu dong doc ra da khac chuoi
// goc du chua ai go gi, va trang tu "xuat ban" mot thay doi khong ai yeu cau.
d.dat(daXuat.chu.length === 1, `chi ghi ${daXuat.chu.length} chuoi thay doi, khong ghi ca ${tong}`);
d.dat(Object.keys(daXuat.bien).length === 2, `ghi ${Object.keys(daXuat.bien).length} bien`);

// 3. Duyet het tab tren trang tuyen sinh va DEM
const p = await mo(G, '/');
await cho(2000);
const dem = async (re) => p.js(`(()=>{const b=document.body.cloneNode(true);
  b.querySelectorAll('script,style').forEach(s=>s.remove());
  return (b.textContent.match(${re})||[]).length})()`);
d.nhom('Tren trang tuyen sinh, duyet het tab');
const t = { cu: 0, moi: 0, chuCu: 0, chuMoi: 0, nguyen: 0 };
const soTabTrang = await p.js(`document.querySelectorAll('nav button, nav [role=tab]').length`);
for (let i = 0; i < soTabTrang; i++) {
  await p.js(`document.querySelectorAll('nav button, nav [role=tab]')[${i}].click()`);
  await cho(700);
  t.cu += await dem('/06\\.09\\.2026/g');
  t.moi += await dem('/15\\.10\\.2026/g');
  t.chuCu += await dem(new RegExp(chonChu.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g').toString());
  t.chuMoi += await dem('/' + MOI + '/g');
  t.nguyen += await dem('/8 module/g');
}
d.dat(t.cu === 0 && t.moi > 0, `bien khai giang: ${t.cu} cho con ngay cu, ${t.moi} cho da doi`);
d.dat(t.chuCu === 0 && t.chuMoi > 0, `chuoi o tab sau: ${t.chuCu} cho con chu cu, ${t.chuMoi} cho da doi`);
// Khop CA node chu khong khop mot phan: neu khop mot phan thi chuoi "8" se sua nham vao
// "8 module" va hang loat cho khac.
d.dat(t.nguyen > 0, `chuoi ngan khong sua nham vao cau khac ("8 module" con ${t.nguyen} cho)`);

await p.js(`document.querySelectorAll('nav button, nav [role=tab]')[0].click()`);
await cho(800);
d.dat((await p.js(`[...document.querySelectorAll('*')].some(e=>e.tagName==='B'&&e.textContent==='Chữ mới')`)) === false,
  'chuoi co the HTML khong sinh ra the that');
d.dat((await dem('/bChữ mới\\/b nhé/g')) > 0, 'the bi loc thanh chu thuong');
d.dat(p.loi.length === 0, 'khong co loi console tren trang tuyen sinh'
  + (p.loi.length ? ': ' + p.loi[0] : ''));

// 4. Hoan ve mac dinh
await q.js(`document.getElementById('hoanNoiDung').click()`);
await cho(300);
await p.js(`location.reload()`);
await cho(2200);
d.dat((await dem('/06\\.09\\.2026/g')) > 0 && (await dem('/15\\.10\\.2026/g')) === 0,
  'hoan ve mac dinh tra lai dung chu goc');

await p.dong();
await q.dong();
d.ketThuc('Tat ca kiem tra noi dung trang deu dat.');

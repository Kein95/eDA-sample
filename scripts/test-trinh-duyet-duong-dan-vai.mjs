// Kiem: moi tab mot duong dan, va tab hien ra dung theo vai.
//
// Bo kiem nay sinh ra sau khi mot ban sua tuong la xong: no bat duoc rang o chon vai hien
// sai vai ngay luc mo, va rang F5 tai duong dan con tra ve TRANG TUYEN SINH chu khong phai
// trang quan tri (nginx khop chinh xac "= /dashboard").
import { mo, cho, boDem, goc } from './lib-trinh-duyet.mjs';

const G = goc();
const d = boDem();
const tabDangMo = (q) => q.js(`(document.querySelector('.tab.on')||{}).dataset?.tab`);
const duongDan = (q) => q.js(`location.pathname`);
const tabHien = (q) => q.js(
  `[...document.querySelectorAll('.tab')].filter(t=>!t.classList.contains('hide')).map(t=>t.dataset.tab)`);
const nhu = (a, b) => JSON.stringify(a) === JSON.stringify(b);

d.nhom('Moi tab mot duong dan');
{
  const q = await mo(G, '/dashboard');
  await q.doi(`typeof LA_DASHBOARD !== 'undefined'`);
  await cho(600);
  d.dat((await duongDan(q)) === '/dashboard/list', `vao /dashboard -> ${await duongDan(q)}`);

  await q.js(`document.querySelector('[data-tab=noidung]').click()`); await cho(400);
  d.dat((await duongDan(q)) === '/dashboard/web', `bam tab Noi dung -> ${await duongDan(q)}`);

  await q.js(`document.querySelector('[data-tab=nhatky]').click()`); await cho(300);
  d.dat((await duongDan(q)) === '/dashboard/log', `bam tab Nhat ky -> ${await duongDan(q)}`);

  // F5 that su, khong phai dieu huong trong trang: day la cho nginx va _redirects phai
  // dung, va cung la cho duong dan import tuong doi tung lam ca trang chet trang.
  await q.send('Page.navigate', { url: G + '/dashboard/log' });
  await cho(2500);
  d.dat((await tabDangMo(q)) === 'nhatky', 'F5 tai /dashboard/log -> van o tab Nhat ky');
  d.dat(q.loi.filter(l => /module|MIME/i.test(l)).length === 0,
    'F5 o duong dan con khong lam hong viec nap module');

  await q.js(`history.back()`); await cho(500);
  d.dat((await tabDangMo(q)) !== undefined, `bam Back -> tab ${await tabDangMo(q)}`);
  await q.dong();
}

d.nhom('Duong dan la thi roi ve tab dau');
{
  const q = await mo(G, '/dashboard/khong-co-tab-nay');
  await q.doi(`typeof LA_DASHBOARD !== 'undefined'`);
  await cho(900);
  d.dat((await tabDangMo(q)) === 'dangky', 'duong dan khong hop le -> mo tab Dang ky');
  d.dat((await duongDan(q)) === '/dashboard/list', 'va sua luon thanh dan cho dung');
  await q.dong();
}

d.nhom('Tab hien ra theo vai');
{
  const q = await mo(G, '/dashboard');
  await q.doi(`typeof LA_DASHBOARD !== 'undefined'`);
  // Doi quet xong roi moi kiem o sua noi dung: quet la nhung ca trang tuyen sinh roi bam
  // qua tung tab, tren ban live mat vai giay. Khong doi thi bang con rong va phep dem
  // "co bao nhieu o sua duoc" tra ve 0 - bo kiem bao hong trong khi trang van dung.
  await q.doi(`gocTheoTab.length && document.querySelectorAll('#dongNoiDung textarea').length`, 60);
  await cho(600);
  d.dat(nhu(await tabHien(q), ['dangky', 'doisoat', 'noidung', 'taikhoan', 'nhatky']),
    'admin thay du 5 tab');
  // O chon phai khop vai dang ap. Lech thi chon dung vai do khong kich hoat su kien
  // change, bam vao khong co gi xay ra.
  d.dat((await q.js(`document.getElementById('doiVai').value`)) === 'EDA_ADMIN',
    'o chon vai hien dung vai dang ap');

  const doiVai = async (v) => {
    await q.js(`(()=>{const s=document.getElementById('doiVai'); s.value=${JSON.stringify(v)}; s.onchange();})()`);
    await cho(500);
  };

  await doiVai('EDA_ACCOUNTANT');
  d.dat(nhu(await tabHien(q), ['dangky', 'doisoat', 'noidung']),
    'ke toan thay 3 tab, khong thay Tai khoan va Nhat ky');
  d.dat((await q.js(`getComputedStyle(document.querySelector('th.cot-tien')).display`)) !== 'none',
    'ke toan VAN thay cot Hoc phi');
  d.dat((await q.js(`document.querySelectorAll('#dongNoiDung textarea:not([readonly])').length`)) === 0,
    'ke toan khong sua duoc noi dung trang');
  d.dat((await q.js(`getComputedStyle(document.getElementById('xuatBan')).display`)) === 'none',
    'ke toan khong thay nut Xuat ban');

  await doiVai('EDA_TA');
  d.dat(nhu(await tabHien(q), ['dangky', 'noidung']),
    'tro giang thay 2 tab, khong thay Doi soat');
  d.dat((await q.js(`getComputedStyle(document.querySelector('th.cot-tien')).display`)) === 'none',
    'tro giang KHONG thay cot Hoc phi');
  const soO = await q.js(`document.querySelectorAll('#rows td.cot-tien').length`);
  const anHet = await q.js(
    `[...document.querySelectorAll('#rows td.cot-tien')].every(td=>getComputedStyle(td).display==='none')`);
  d.dat(soO > 0 && anHet, `moi o trong cot Hoc phi cung an (${soO} o), khong chi tieu de`);

  // Dang dung o tab bi cam thi phai bi day ra, VA duong dan phai theo: lech thi thanh dia
  // chi ghi mot tab con man hinh hien tab khac, va lech do song qua ca F5.
  await q.js(`document.getElementById('doiVai').value='EDA_ADMIN'; document.getElementById('doiVai').onchange()`);
  await cho(300);
  await q.js(`document.querySelector('[data-tab=nhatky]').click()`); await cho(300);
  await doiVai('EDA_TA');
  d.dat((await tabDangMo(q)) === 'dangky', 'dang o tab cam -> bi day ve tab duoc phep');
  d.dat((await duongDan(q)) === '/dashboard/list', 'va duong dan doi theo, khong de lech');

  await doiVai('EDA_ADMIN');
  d.dat((await q.js(`document.querySelectorAll('#dongNoiDung textarea:not([readonly])').length`)) > 0,
    'quay lai admin thi sua duoc noi dung trang');
  d.dat(q.loi.length === 0, 'khong co loi console' + (q.loi.length ? ': ' + q.loi[0] : ''));
  await q.dong();
}

d.ketThuc('Tat ca kiem tra duong dan va vai deu dat.');

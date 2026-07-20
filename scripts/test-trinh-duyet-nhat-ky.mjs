// Kiem hai nut tai nhat ky: dung pham vi dang loc, va chan cong thuc Excel.
//
// Pham vi la cho de sai nhat: loc theo mot nguoi roi bam tai ma ra ca so thi nguoi tai
// tuong minh dang cam ban da loc, va doc sai pham vi ma khong biet.
import { mo, cho, boDem, goc } from './lib-trinh-duyet.mjs';

const G = goc();
const d = boDem();
const NHIEU_DONG = 'dong 1\ndong 2';

const q = await mo(G, '/dashboard/log');
await q.doi(`typeof LA_DASHBOARD !== 'undefined'`);
await q.send('Browser.setDownloadBehavior', { behavior: 'deny' });   // khong ghi ra o dia
await cho(1200);

// Bat noi dung tep thay vi de trinh duyet tai ve
await q.js(`(()=>{ window.__bat = null;
  const goc = URL.createObjectURL.bind(URL);
  URL.createObjectURL = (b) => { window.__bat = b; return goc(b); };
})()`);
const layTep = async (nut) => {
  await q.js(`window.__bat = null; document.getElementById(${JSON.stringify(nut)}).click()`);
  await cho(300);
  return q.js(`window.__bat ? window.__bat.text() : null`);
};
const thanTxt = (s) => s.split('\n').filter((x) => /^\d{1,4}[.\/-]\d/.test(x));

await q.js(`ghiLog('=SUM(A1)', 'thu chan cong thuc Excel');
  ghiLog('Ghi chu nhieu dong', ${JSON.stringify(NHIEU_DONG)}); veNhatKy()`);
await cho(300);
// Dem TRUOC khi bam tai: chinh nut tai cung ghi mot dong nhat ky.
const tong = await q.js(`nhatKy.length`);

d.nhom('Tai ca so');
const csv = await layTep('taiLog');
d.dat(csv !== null && csv.trim().split('\r\n').length - 1 === tong,
  `CSV co ${csv ? csv.trim().split('\r\n').length - 1 : '?'} dong + tieu de (nhat ky ${tong})`);
// Phai doc BYTE THO: Blob.text() giai ma UTF-8 va CAT BOM di theo dung chuan, nen doc
// bang text() thi khong bao gio thay BOM du no co that trong tep.
const byteDau = await q.js(`window.__bat.arrayBuffer().then(b => [...new Uint8Array(b).slice(0,3)])`);
d.dat(String(byteDau) === '239,187,191', `CSV co BOM cho Excel doc dung tieng Viet (${byteDau})`);
d.dat(/"'=SUM\(A1\)"/.test(csv), 'CSV chan cong thuc Excel (=SUM bi them dau nhay)');

const tong2 = await q.js(`nhatKy.length`);
const txt = await layTep('taiLogTxt');
d.dat(txt !== null && txt.includes('Nhật ký eDA 2026'), 'TXT co dong tieu de');
d.dat(thanTxt(txt).length === tong2, `TXT co ${thanTxt(txt).length} dong than (nhat ky ${tong2})`);
d.dat(!txt.includes(NHIEU_DONG), 'TXT gop chi tiet nhieu dong thanh MOT dong');
d.dat(txt.includes('dong 1 dong 2'), 'TXT giu du chu khi gop dong');
// Ten tep theo ngay MAY, khong theo UTC: lech mui gio thi ten tep va dong "Xuat luc" ben
// trong ghi hai ngay khac nhau trong cung mot tep dung de doi chieu. Bat ten tep bang cach
// chan chinh cu bam vao the <a>.
const tenTep = await q.js(`(()=>{
  const goc = HTMLAnchorElement.prototype.click;
  let ten = '';
  HTMLAnchorElement.prototype.click = function () { ten = this.download; };
  document.getElementById('taiLogTxt').click();
  HTMLAnchorElement.prototype.click = goc;
  return ten;
})()`);
const ngayMay = await q.js(`(()=>{const d=new Date();
  return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')})()`);
d.dat(tenTep === `nhat-ky-eda-${ngayMay}.txt`,
  `ten tep theo ngay may: ${tenTep} (hom nay ${ngayMay})`);

d.nhom('Loc roi tai: phai chi ra phan da loc');
await q.js(`o('timLog').value = 'Excel'; veNhatKy()`);
await cho(300);
const soLoc = await q.js(`nhatKyDangXem().length`);
const tongLuc = await q.js(`nhatKy.length`);
d.dat(soLoc > 0 && soLoc < tongLuc, `loc con ${soLoc}/${tongLuc} dong`);
const csv2 = await layTep('taiLog');
d.dat(csv2.trim().split('\r\n').length - 1 === soLoc,
  `CSV sau khi loc co ${csv2.trim().split('\r\n').length - 1} dong (mong doi ${soLoc})`);
const soLoc2 = await q.js(`nhatKyDangXem().length`);
const txt2 = await layTep('taiLogTxt');
d.dat(thanTxt(txt2).length === soLoc2, `TXT sau khi loc co ${thanTxt(txt2).length} dong (mong doi ${soLoc2})`);
d.dat(/đã lọc/.test(txt2), 'TXT ghi ro la ban DA LOC va loc bang gi');

d.nhom('Loc den rong');
await q.js(`o('timLog').value = 'khong-co-chuoi-nay-dau-nhe'; veNhatKy()`);
await cho(300);
const txt3 = await layTep('taiLogTxt');
d.dat(txt3 !== null && txt3.includes('không có dòng nào'), 'khong con dong nao thi TXT van tai duoc');
const csv3 = await layTep('taiLog');
d.dat(csv3 !== null && csv3.trim().split('\r\n').length === 1, 'CSV rong chi con dong tieu de');

d.dat(q.loi.length === 0, 'khong co loi console' + (q.loi.length ? ': ' + q.loi[0] : ''));
await q.dong();
d.ketThuc('Tat ca kiem tra xuat nhat ky deu dat.');

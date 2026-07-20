// Kiem bo doc sao ke chung. Chay bang:
//   node scripts/test-doc-sao-ke.mjs
//
// Y do: khong ngan hang nao duoc hardcode. Cac sao ke gia duoi day co bo cuc KHAC NHAU
// (ten cot, thu tu cot, so hang rac o dau, kieu ngay, kieu so, dau phan cach) va bo doc
// phai xu ly duoc het chi bang anh xa cot.
import assert from 'node:assert/strict';
import {
  boDau, docBang, doanDauPhanCach, timDongTieuDe, doanAnhXa, docSoTien, docNgay,
  apDungAnhXa, docTuDong,
} from '../supabase/functions/_shared/doc-sao-ke.js';

let so = 0;
const test = (ten, fn) => { fn(); so++; console.log('  ok  ' + ten); };

// ── 1. Bo dau ──────────────────────────────────────────────────────────────
test('boDau bo dau tieng Viet', () => {
  assert.equal(boDau('Ngày giao dịch'), 'ngay giao dich');
  assert.equal(boDau('Số tiền ghi có'), 'so tien ghi co');
  assert.equal(boDau('ĐỒNG'), 'dong');
});

// ── 2. Doc so tien kieu Viet Nam ───────────────────────────────────────────
test('doc so tien voi dau cham ngan cach nghin', () => {
  assert.equal(docSoTien('4.000.000'), 4000000);
  assert.equal(docSoTien('26.000.000'), 26000000);
});

test('doc so tien voi dau phay ngan cach nghin', () => {
  assert.equal(docSoTien('4,000,000'), 4000000);
  assert.equal(docSoTien('12,500,000'), 12500000);
});

test('doc so tien co ca hai dau: dau sau cung la thap phan', () => {
  assert.equal(docSoTien('4,000,000.00'), 4000000);
  assert.equal(docSoTien('4.000.000,50'), 4000000.5);
});

test('mot dau phan cach + 3 chu so = ngan cach nghin, khong phai thap phan', () => {
  // "1.234" trong sao ke Viet Nam luon la mot nghin hai tram ba muoi tu
  assert.equal(docSoTien('1.234'), 1234);
  assert.equal(docSoTien('1,234'), 1234);
});

test('mot dau phan cach + 2 chu so = thap phan', () => {
  assert.equal(docSoTien('1.50'), 1.5);
});

test('chuoi hinh dang NGAY khong duoc doc thanh so tien', () => {
  // Anh xa nham cot Ngay vao cot Tien vao: neu chi boc ky tu la thi "2026-07-03" thanh
  // hai muoi trieu va "03/07/2026" thanh ba trieu - sai so tien ma khong bao loi gi.
  assert.equal(docSoTien('2026-07-03'), NaN);
  assert.equal(docSoTien('03/07/2026'), NaN);
  assert.equal(docSoTien('03/07/2026 14:35'), NaN);
  // Nhung so am that thi van doc duoc: dau tru chi o dau chuoi
  assert.equal(docSoTien('-55000'), -55000);
});

test('doc so tien am va co ky tu la', () => {
  assert.equal(docSoTien('-55,000'), -55000);
  assert.equal(docSoTien('4.000.000 VND'), 4000000);
  assert.equal(docSoTien(''), NaN);
  assert.equal(docSoTien('   '), NaN);
});

// ── 3. Doc ngay ────────────────────────────────────────────────────────────
test('ngay Viet Nam dd/mm/yyyy doc dung THANG', () => {
  // Doan nham thanh mm/dd thi 03/07 ra mung 7 thang 3 - lech 4 thang ma nhin khong ra
  assert.equal(docNgay('03/07/2026').slice(0, 10), '2026-07-03');
  assert.equal(docNgay('20-07-2026').slice(0, 10), '2026-07-20');
  assert.equal(docNgay('03.07.2026').slice(0, 10), '2026-07-03');
});

test('ngay ISO yyyy-mm-dd', () => {
  assert.equal(docNgay('2026-07-03').slice(0, 10), '2026-07-03');
});

test('nam 2 chu so', () => {
  assert.equal(docNgay('03/07/26').slice(0, 10), '2026-07-03');
});

test('ngay kem gio', () => {
  assert.equal(docNgay('03/07/2026 14:35').slice(0, 16), '2026-07-03T14:35');
});

test('ngay khong doc duoc tra ve null', () => {
  assert.equal(docNgay(''), null);
  assert.equal(docNgay('khong phai ngay'), null);
});

// ── 4. Ba sao ke bo cuc khac han nhau ──────────────────────────────────────
// Kieu A: co 4 hang rac o dau, cot ghi no va ghi co rieng, ngay dd/mm/yyyy
const SAO_KE_A = `SAO KE TAI KHOAN
Chu tai khoan: CONG TY ABC
So tai khoan: 001100223344
Tu ngay 01/07/2026 den 20/07/2026

STT,Ngay giao dich,So tham chieu,Ghi no,Ghi co,Noi dung chi tiet
1,03/07/2026,FT26185001,,"4.000.000","CK eDA26-ABC123 0900000001"
2,05/07/2026,FT26186002,"55.000",,"PHI CHUYEN TIEN"
3,07/07/2026,FT26187003,,"12.000.000","EDA26XYZ7890900000002 NOP HOC PHI"`;

// Kieu B: tieu de ngay hang dau, tieng Anh, mot cot so tien co dau, ngay ISO, dau ;
const SAO_KE_B = `Transaction Date;Reference;Amount;Description
2026-07-03;REF001;4,000,000;CK eDA26-ABC123
2026-07-05;REF002;-55,000;SERVICE FEE
2026-07-07;REF003;12,000,000;eDA26-XYZ789 hoc phi`;

// Kieu C: khong co cot ma giao dich, ten cot khac han, co dau tieng Viet day du
const SAO_KE_C = `Ngày,Diễn giải,Số tiền ghi nợ,Số tiền ghi có
20/07/2026,"Nộp học phí eDA26-KKK111",,"4.000.000"
20/07/2026,"Rút tiền","1.000.000",`;

test('kieu A: tim dung hang tieu de du co 5 hang rac o dau', () => {
  const luoi = docBang(SAO_KE_A);
  assert.equal(timDongTieuDe(luoi), 5);
});

test('kieu A: doan dung tung cot', () => {
  const luoi = docBang(SAO_KE_A);
  const a = doanAnhXa(luoi[5]);
  assert.equal(a.ngay, 1);
  assert.equal(a.ma_gd, 2);
  assert.equal(a.tien_ra, 3);
  assert.equal(a.tien_vao, 4);
  assert.equal(a.noi_dung, 5);
});

test('kieu A: chi lay tien vao, bo dong tien ra', () => {
  const { giao_dich, bo } = docTuDong(SAO_KE_A);
  assert.equal(giao_dich.length, 2);
  assert.equal(giao_dich[0].ma_gd, 'FT26185001');
  assert.equal(giao_dich[0].so_tien, 4000000);
  assert.equal(giao_dich[0].posted_at.slice(0, 10), '2026-07-03');
  assert.ok(bo.some((b) => b.ly_do === 'tien ra'), 'khong bao ly do bo dong tien ra');
});

test('kieu B: dau cham phay, mot cot so tien co dau, ngay ISO', () => {
  const { giao_dich } = docTuDong(SAO_KE_B);
  assert.equal(giao_dich.length, 2, 'phai bo dong -55,000');
  assert.equal(giao_dich[0].so_tien, 4000000);
  assert.equal(giao_dich[1].so_tien, 12000000);
});

test('kieu C: ten cot co dau day du van nhan ra', () => {
  const { giao_dich, anhXa } = docTuDong(SAO_KE_C);
  assert.equal(anhXa.ma_gd, null, 'sao ke nay khong co cot ma giao dich');
  assert.equal(giao_dich.length, 1);
  assert.equal(giao_dich[0].so_tien, 4000000);
  assert.equal(giao_dich[0].ma_la_thay_the, true, 'phai danh dau ma la khoa thay the');
});

test('cot ghi no KHONG bi nhan nham thanh cot tien vao', () => {
  // "So tien ghi no" chua ca "so tien" - neu tim tu khoa chung chung truoc thi vo nham
  const luoi = docBang(SAO_KE_C);
  const a = doanAnhXa(luoi[0]);
  assert.equal(a.tien_ra, 2);
  assert.equal(a.tien_vao, 3);
});

// ── 4b. Hang tieu de CHEP DUNG tu sao ke Vietcombank that ──────────────────
// Chi lay hang TIEU DE tu file that (khong phai du lieu ca nhan). Day la bo cuc kho
// nhat gap phai: tieu de song ngu co XUONG DONG ngay trong o, cot "Ngay" gop chung voi
// "So CT" trong mot o, va cot "So du" nam ngay canh cot "Ghi co".
const TIEU_DE_VCB = [
  'STT\nNo.',
  'Ngày1/\nTNX Date/ Số CT/ Doc No',
  'Ngày hiệu lực2/\nEffective date',
  'Số tiền ghi nợ/\nDebit',
  'Số tiền ghi có/\nCredit',
  'Số dư/\nBalance',
  'Nội dung chi tiết/\nTransactions in detail',
];

test('tieu de Vietcombank that: doan dung tung cot', () => {
  const a = doanAnhXa(TIEU_DE_VCB);
  assert.equal(a.tien_vao, 4, 'phai la cot Ghi co');
  assert.equal(a.tien_ra, 3, 'phai la cot Ghi no');
  assert.equal(a.noi_dung, 6);
  assert.notEqual(a.tien_vao, 5, 'KHONG duoc lay cot So du lam tien vao');
  assert.notEqual(a.ngay, null);
  assert.notEqual(a.ma_gd, null);
});

test('cot So du KHONG bao gio bi lay lam so tien', () => {
  // Lay nham cot So du thi moi giao dich deu mang so du tai khoan - sai hoan toan
  // nhung van la so duong hop le nen khong co gi bao loi.
  const a = doanAnhXa(TIEU_DE_VCB);
  for (const k of ['tien_vao', 'tien_ra']) assert.notEqual(a[k], 5);
});

test('tieu de xuong dong trong o khong lam hong viec tim hang tieu de', () => {
  const luoi = [['SAO KÊ TÀI KHOẢN'], [''], ['Chủ tài khoản/ Account name:', 'X'],
                TIEU_DE_VCB, ['1', '31/10/2025 / 0001 - 12345', '31/10/2025', '', '500,000',
                              '900,000,000', 'CK eDA26-ABC123']];
  assert.equal(timDongTieuDe(luoi), 3);
  const { giao_dich } = apDungAnhXa(luoi, { dongTieuDe: 3, ...doanAnhXa(TIEU_DE_VCB) });
  assert.equal(giao_dich.length, 1);
  assert.equal(giao_dich[0].so_tien, 500000, 'phai lay Ghi co, khong phai So du');
  assert.equal(giao_dich[0].posted_at.slice(0, 10), '2025-10-31');
});

// ── 5. Nguoi tu chon cot khi doan sai ──────────────────────────────────────
test('anh xa do nguoi dat de len ket qua doan', () => {
  const luoi = docBang(SAO_KE_B);
  // Gia su nguoi doi cot noi dung sang cot khac
  const { giao_dich } = apDungAnhXa(luoi,
    { dongTieuDe: 0, ma_gd: 1, ngay: 0, tien_vao: 2, tien_ra: null, noi_dung: 1 });
  assert.equal(giao_dich[0].noi_dung, 'REF001');
});

test('sao ke khong nhan ra duoc thi bao ro, khong tra ve mang rong im lang', () => {
  const kq = docTuDong('mot hai ba\nbon nam sau');
  assert.equal(kq.dongTieuDe, -1, 'phai bao la khong tim duoc hang tieu de');
  assert.deepEqual(kq.giao_dich, []);
});

test('dong bi bo deu co ly do, khong bien mat im lang', () => {
  const { bo } = docTuDong(SAO_KE_A);
  assert.ok(bo.length > 0);
  for (const b of bo) {
    assert.ok(b.hang > 0, 'thieu so hang');
    assert.ok(b.ly_do, 'thieu ly do');
  }
});

// ── 6. Dau phan cach ───────────────────────────────────────────────────────
test('doan dung dau phan cach', () => {
  assert.equal(doanDauPhanCach(SAO_KE_A), ',');
  assert.equal(doanDauPhanCach(SAO_KE_B), ';');
  assert.equal(doanDauPhanCach('a\tb\tc\n1\t2\t3'), '\t');
  assert.equal(doanDauPhanCach('chi mot cot'), ',');   // khong co dau nao -> mac dinh
});

test('so tien co dau phay KHONG bi xe o trong file dung cham phay', () => {
  // Day la lo hong that: neu coi ca "," va ";" deu la dau phan cach thi "4,000,000"
  // thanh ba o va so tien 4 trieu doc ra thanh 4.
  const luoi = docBang('Ngay;Ref;Amount;Noi dung\n03/07/2026;R1;4,000,000;CK');
  assert.equal(luoi[1].length, 4, 'o so tien bi xe ra');
  assert.equal(luoi[1][2], '4,000,000');
});

test('dau phay trong dau nhay kep khong lam doan nham dau phan cach', () => {
  const s = 'Ngay;Ref;Amount;Noi dung\n03/07/2026;R1;1000;"a,b,c,d,e,f,g"';
  assert.equal(doanDauPhanCach(s), ';');
});

// ── 7. Nhung thu de lam vo bo doc ──────────────────────────────────────────
test('o co dau phay trong dau nhay kep khong lam lech cot', () => {
  const { giao_dich } = docTuDong(
    'Ngay,Ref,Ghi co,Noi dung\n03/07/2026,R1,"4.000.000","CK eDA26-ABC123, dot 1"');
  assert.equal(giao_dich[0].noi_dung, 'CK eDA26-ABC123, dot 1');
});

test('o co dau nhay kep long nhau', () => {
  const { giao_dich } = docTuDong(
    'Ngay,Ref,Ghi co,Noi dung\n03/07/2026,R1,"4.000.000","CK ""gap"" hoc phi"');
  assert.equal(giao_dich[0].noi_dung, 'CK "gap" hoc phi');
});

test('hang trong giua file bi bo qua', () => {
  const { giao_dich } = docTuDong(
    'Ngay,Ref,Ghi co,Noi dung\n\n03/07/2026,R1,"4.000.000","x"\n\n');
  assert.equal(giao_dich.length, 1);
});

test('file rong khong lam no', () => {
  assert.deepEqual(docTuDong('').giao_dich, []);
  assert.deepEqual(docBang(''), []);
});

console.log('\n' + so + ' kiem tra deu dat.');

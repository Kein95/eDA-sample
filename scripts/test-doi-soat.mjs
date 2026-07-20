// Kiem logic doi soat sao ke. Chay bang:
//   node scripts/test-doi-soat.mjs
//
// Test CHINH cua file nay la "upload lai cung mot file khong cong tien lan hai".
// Do la lo hong that su cua VNCLO (khong co bang giao dich), va la thu de sai nhat khi
// them nhieu dot dong tien.
import assert from 'node:assert/strict';
import {
  bocKhoa, chuanHoaSdt, dotCanThu, khopGiaoDich, locGiaoDichMoi, maThayThe,
} from '../supabase/functions/_shared/doi-soat.js';

let so = 0;
const test = (ten, fn) => { fn(); so++; console.log('  ok  ' + ten); };
const testAsync = async (ten, fn) => { await fn(); so++; console.log('  ok  ' + ten); };

// ── Danh ba mau ────────────────────────────────────────────────────────────
const dot = (thu_tu, so_tien, da_thu = 0, mien_giam = 0) =>
  ({ id: `d${thu_tu}`, thu_tu, so_tien, mien_giam, da_thu });

const nguoi = (id, code, phone, dots) => ({ id, code, phone, dots });

const DANH_BA = [
  nguoi('r1', 'eDA26-ABC123', '0900000001', [dot(1, 4_000_000), dot(2, 20_000_000)]),
  nguoi('r2', 'eDA26-XYZ789', '0900000002', [dot(1, 4_000_000, 4_000_000), dot(2, 12_000_000)]),
  nguoi('r3', 'eDA26-KKK111', '0900000003', []),                       // chua chon phuong an
  nguoi('r4', 'eDA26-QQQ222', '0900000004', [dot(1, 4_000_000, 4_000_000)]), // da dong du
];

const gd = (ma_gd, so_tien, noi_dung, posted_at = '2026-07-20T03:00:00Z') =>
  ({ ma_gd, posted_at, so_tien, noi_dung });

// ── 1. Boc khoa tu noi dung chuyen khoan ───────────────────────────────────
test('boc duoc ca ma lan SDT tu noi dung chuan', () => {
  const k = bocKhoa('CK eDA26-ABC123 0900000001 hoc phi dot 1');
  assert.equal(k.ma, 'eDA26-ABC123');
  assert.equal(k.sdt, '0900000001');
});

test('ngan hang VIET HOA va boc dau cach van boc duoc', () => {
  // Nhieu ngan hang tra ve noi dung da viet hoa va dinh lien
  const k = bocKhoa('CHUYEN TIEN EDA26ABC1230900000001 ND HOC PHI');
  assert.equal(k.ma, 'eDA26-ABC123');
  assert.equal(k.sdt, '0900000001');
});

test('chi co SDT, khong co ma', () => {
  const k = bocKhoa('nop hoc phi 0900000002');
  assert.equal(k.ma, null);
  assert.equal(k.sdt, '0900000002');
});

test('khong co gi nhan ra duoc', () => {
  const k = bocKhoa('CHUYEN KHOAN');
  assert.deepEqual(k, { ma: null, sdt: null });
});

test('so 11 chu so khong bi nhan nham la SDT', () => {
  assert.equal(bocKhoa('GD 09001234567').sdt, null);
});

test('SDT go co dau cach hoac dau cham van boc duoc', () => {
  // Nguoi ta go the nay rat nhieu va ngan hang giu nguyen
  assert.equal(bocKhoa('nop hoc phi 0900 0000 07').sdt, '0900000007');
  assert.equal(bocKhoa('nop hoc phi 0900.000.007').sdt, '0900000007');
  assert.equal(bocKhoa('nop hoc phi 0900-000-007').sdt, '0900000007');
});

test('khong cat nham phan duoi cua so tien thanh SDT', () => {
  // "5000000 0900000007": neu thieu chan ranh gioi dau thi se khop tu giua so tien
  assert.equal(bocKhoa('CK 5000000 0900000007 hoc phi').sdt, '0900000007');
  assert.equal(bocKhoa('so tien 50000000900000007').sdt, null);
});

test('chuanHoaSdt bo dau cach va dau cham', () => {
  assert.equal(chuanHoaSdt('0900 0000 01'), '0900000001');
  assert.equal(chuanHoaSdt('0900.0000.01'), '0900000001');
});

// ── 2. Chon dot de gan tien ────────────────────────────────────────────────
test('gan vao dot chua thu du co thu tu nho nhat', () => {
  assert.equal(dotCanThu(DANH_BA[0].dots).thu_tu, 1);
  assert.equal(dotCanThu(DANH_BA[1].dots).thu_tu, 2);   // dot 1 da dong xong
});

test('da dong du het thi khong con dot nao', () => {
  assert.equal(dotCanThu(DANH_BA[3].dots), null);
});

test('mien giam lam dot coi nhu da du', () => {
  assert.equal(dotCanThu([dot(1, 4_000_000, 0, 4_000_000)]), null);
});

// ── 3. Khop giao dich ──────────────────────────────────────────────────────
test('khop bang ma, dung so tien -> tick san', () => {
  const k = khopGiaoDich(gd('G1', 4_000_000, 'eDA26-ABC123 0900000001'), DANH_BA);
  assert.equal(k.registration_id, 'r1');
  assert.equal(k.installment_id, 'd1');
  assert.equal(k.khop_kieu, 'ma');
  assert.deepEqual(k.canh_bao, []);
  assert.equal(k.tick_san, true);
});

test('ma sai nhung SDT dung -> van khop, KHONG tick san', () => {
  // Mot phu huynh co the dang ky cho hai con bang cung mot so, nen SDT khong xac dinh
  // duy nhat mot nguoi. Phai de nguoi tu quyet.
  const k = khopGiaoDich(gd('G2', 4_000_000, 'nop tien 0900000001'), DANH_BA);
  assert.equal(k.registration_id, 'r1');
  assert.equal(k.khop_kieu, 'sdt');
  assert.equal(k.tick_san, false);
});

test('thieu tien -> van khop nhung canh bao va khong tick san', () => {
  const k = khopGiaoDich(gd('G3', 3_000_000, 'eDA26-ABC123'), DANH_BA);
  assert.equal(k.installment_id, 'd1');
  assert.deepEqual(k.canh_bao, ['thieu_tien']);
  assert.equal(k.tick_san, false);
});

test('thua tien -> canh bao, khong tu chia sang dot sau', () => {
  const k = khopGiaoDich(gd('G4', 24_000_000, 'eDA26-ABC123'), DANH_BA);
  assert.equal(k.installment_id, 'd1');          // van chi gan vao dot 1
  assert.deepEqual(k.canh_bao, ['thua_tien']);
  assert.equal(k.tick_san, false);
});

test('khong nhan ra ai -> khong gan bua vao nguoi nao', () => {
  const k = khopGiaoDich(gd('G5', 4_000_000, 'CHUYEN KHOAN'), DANH_BA);
  assert.equal(k.registration_id, null);
  assert.equal(k.installment_id, null);
  assert.equal(k.tick_san, false);
});

test('nguoi chua chon phuong an -> khop duoc nguoi, khong co dot', () => {
  const k = khopGiaoDich(gd('G6', 4_000_000, 'eDA26-KKK111'), DANH_BA);
  assert.equal(k.registration_id, 'r3');
  assert.equal(k.installment_id, null);
  assert.deepEqual(k.canh_bao, ['chua_chon_phuong_an']);
});

test('da dong du ma van chuyen them -> canh bao, khong gan', () => {
  const k = khopGiaoDich(gd('G7', 1_000_000, 'eDA26-QQQ222'), DANH_BA);
  assert.equal(k.registration_id, 'r4');
  assert.equal(k.installment_id, null);
  assert.deepEqual(k.canh_bao, ['khong_co_dot']);
});

// ── 4. Chong dem tien hai lan ──────────────────────────────────────────────
test('upload lai cung mot lo -> lan hai khong con giao dich moi nao', () => {
  const lo = [gd('G1', 4_000_000, 'eDA26-ABC123'), gd('G2', 12_000_000, 'eDA26-XYZ789')];

  const lan1 = locGiaoDichMoi(lo, new Set());
  assert.equal(lan1.moi.length, 2);
  assert.equal(lan1.daXuLy.length, 0);

  // Sau lan 1, DB da co hai ma nay
  const daCo = new Set(lan1.moi.map((t) => t.ma_gd));

  const lan2 = locGiaoDichMoi(lo, daCo);
  assert.equal(lan2.moi.length, 0, 'upload lai van sinh giao dich moi = se cong tien hai lan');
  assert.equal(lan2.daXuLy.length, 2);
});

test('hai file sao ke chong lan nhau -> phan chung chi tinh mot lan', () => {
  const thang3 = [gd('A1', 4_000_000, 'eDA26-ABC123'), gd('A2', 4_000_000, 'eDA26-XYZ789')];
  const quy1 = [...thang3, gd('A3', 4_000_000, 'eDA26-KKK111')];   // chua ca thang 3

  const daCo = new Set(locGiaoDichMoi(thang3, new Set()).moi.map((t) => t.ma_gd));
  const sau = locGiaoDichMoi(quy1, daCo);
  assert.equal(sau.moi.length, 1);
  assert.equal(sau.moi[0].ma_gd, 'A3');
});

test('dong trung ngay TRONG mot file cung chi tinh mot lan', () => {
  const lo = [gd('B1', 4_000_000, 'x'), gd('B1', 4_000_000, 'x')];
  const kq = locGiaoDichMoi(lo, new Set());
  assert.equal(kq.moi.length, 1);
  assert.equal(kq.daXuLy.length, 1);
});

await testAsync('ma thay the on dinh voi cung du lieu, khac khi du lieu khac', async () => {
  const a = { posted_at: '2026-07-20T03:00:00Z', so_tien: 4_000_000, noi_dung: 'eDA26-ABC123' };
  assert.equal(await maThayThe(a), await maThayThe(a));
  assert.notEqual(await maThayThe(a), await maThayThe({ ...a, so_tien: 4_000_001 }));
});

console.log('');
console.log(so + ' kiem tra deu dat.');

// Logic doi soat sao ke. Khong dung DB, khong dung API rieng cua Deno hay cua trinh duyet.
//
// Viet bang .js chu khong phai .ts CO Y: ba noi dung chung DUNG MOT BAN nay -
//   - edge function eda-doi-soat (Deno import truc tiep)
//   - tab Doi soat trong admin.html (trinh duyet import truc tiep)
//   - scripts/test-doi-soat.mjs (Node import truc tiep)
// Neu de .ts thi trinh duyet khong nap duoc, phai bien dich hoac chep tay ra ban thu hai,
// va ban demo se troi khac ban that luc nao khong biet.
//
// Moi ham o day la ham thuan: dua vao giao dich + danh ba, tra ve ket qua khop.
// Khong ham nao ghi gi. Viec ghi do phia goi quyet dinh, SAU KHI nguoi da xac nhan.

/**
 * @typedef {{ma_gd:string, posted_at:string, so_tien:number, noi_dung:string}} GiaoDichTho
 * @typedef {{id:string, thu_tu:number, so_tien:number, mien_giam:number, da_thu:number}} DotDong
 * @typedef {{id:string, code:string, phone:string, dots:DotDong[]}} NguoiDangKy
 */

/** Bo dau cach, cham, gach de so sanh SDT: "0900 0000 01" == "0900000001". */
export function chuanHoaSdt(s) {
  return (s || '').replace(/[\s.\-()]/g, '');
}

/**
 * Boc hai khoa tu noi dung chuyen khoan.
 *
 * Nguoi chuyen tien duoc huong dan ghi "<ma> <sdt>" - hai khoa trong mot chuoi de con
 * mot cai khi ho go thieu cai kia. Ngan hang thuong VIET HOA va boc het dau cach, nen
 * khong duoc dua vao dau cach de tach.
 */
export function bocKhoa(noiDung) {
  const s = (noiDung || '').toUpperCase();
  const mMa = s.match(/EDA26[-\s]?([A-Z0-9]{6})/);

  // Phai CAT phan ma ra truoc khi tim SDT. Ma ket thuc bang chu so (eDA26-ABC123), va
  // ngan hang thuong boc het dau cach, nen chuoi thanh "EDA26ABC1230900000001": chu so
  // cuoi cua ma dinh vao dau SDT, lam mat ranh gioi va SDT khong bao gio bat duoc.
  const conLai = mMa
    ? s.slice(0, mMa.index) + ' ' + s.slice(mMa.index + mMa[0].length)
    : s;

  // Cho phep MOT dau cach / cham / gach giua cac chu so: nguoi ta go "0900 0000 07"
  // hoac "0900.000.007" rat nhieu, va ngan hang giu nguyen nhu ho go.
  //
  // (?:^|\D) o dau la bat buoc: thieu no thi "5000000 0900000007" se khop nham vao
  // phan duoi cua so tien. (?!\d) o cuoi de so 11 chu so khong bi cat 10 dau ra dung.
  const mSdt = conLai.match(/(?:^|\D)(0(?:[ .\-]?\d){9})(?!\d)/);
  return {
    ma: mMa ? 'eDA26-' + mMa[1] : null,
    sdt: mSdt ? chuanHoaSdt(mSdt[1]) : null,
  };
}

/**
 * Sinh khoa thay the khi sao ke KHONG co so tham chieu.
 *
 * Kem hon ma that: hai giao dich giong het nhau trong cung mot giay se bi coi la mot.
 * Nhung van hon la khong co khoa nao - khong khoa thi upload lai file cu se cong tien
 * lan hai. Phia goi phai danh dau ro day la khoa thay the, dung im lang.
 */
export async function maThayThe(t) {
  const chuoi = `${t.posted_at}|${t.so_tien}|${t.noi_dung}`;
  const bam = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(chuoi));
  return 'TT-' + [...new Uint8Array(bam)].map((b) => b.toString(16).padStart(2, '0')).join('').slice(0, 24);
}

/** Dot dau tien chua thu du. null = da dong het, hoac chua co dot nao. */
export function dotCanThu(dots) {
  return [...dots]
    .sort((a, b) => a.thu_tu - b.thu_tu)
    .find((d) => d.da_thu < d.so_tien - d.mien_giam) ?? null;
}

/**
 * Khop mot giao dich vao nguoi + dot.
 *
 * Uu tien ma dang ky, truot thi thu SDT. Khop duoc nguoi roi thi gan vao dot chua thu
 * du co thu tu nho nhat.
 *
 * CO Y khong tu chia mot giao dich cho nhieu dot khi nguoi do chuyen gop: doan sai o
 * day la sai so tien, ma nguoi phu trach nhin mot giay la biet. De ho quyet dinh.
 *
 * @param {GiaoDichTho} txn
 * @param {NguoiDangKy[]} danhBa
 */
export function khopGiaoDich(txn, danhBa) {
  const kq = {
    txn, registration_id: null, installment_id: null,
    khop_kieu: null, canh_bao: [], tick_san: false,
  };

  const { ma, sdt } = bocKhoa(txn.noi_dung);
  let nguoi = ma ? danhBa.find((n) => n.code.toUpperCase() === ma.toUpperCase()) : undefined;
  if (nguoi) kq.khop_kieu = 'ma';
  if (!nguoi && sdt) {
    const can = chuanHoaSdt(sdt);
    nguoi = danhBa.find((n) => chuanHoaSdt(n.phone) === can);
    if (nguoi) kq.khop_kieu = 'sdt';
  }
  if (!nguoi) return kq;                       // chua khop duoc ai, de nguyen cho nguoi xu ly

  kq.registration_id = nguoi.id;

  if (!nguoi.dots || nguoi.dots.length === 0) {
    kq.canh_bao.push('chua_chon_phuong_an');
    return kq;
  }
  const dot = dotCanThu(nguoi.dots);
  if (!dot) {
    kq.canh_bao.push('khong_co_dot');          // da dong du roi ma van chuyen them
    return kq;
  }

  kq.installment_id = dot.id;
  const conThieu = dot.so_tien - dot.mien_giam - dot.da_thu;
  if (txn.so_tien < conThieu) kq.canh_bao.push('thieu_tien');
  if (txn.so_tien > conThieu) kq.canh_bao.push('thua_tien');

  // Chi tick san khi khop bang MA va so tien dung khop.
  // Khop bang SDT KHONG tick san: mot phu huynh co the dang ky cho hai con bang cung mot
  // so, luc do SDT khong xac dinh duy nhat mot nguoi. Bang dang ky co y khong dat unique
  // tren phone - xem migration 0001.
  kq.tick_san = kq.khop_kieu === 'ma' && kq.canh_bao.length === 0;
  return kq;
}

/**
 * Tach giao dich moi va giao dich da xu ly tu lan truoc.
 *
 * Day chi la lop bao cho nguoi dung biet "12 dong da xu ly tu lan truoc". Lop THAT SU
 * chan dem trung nam o DB: unique (ngan_hang, ma_gd) trong eda_bank_txn. Dung dua vao
 * ham nay de bao dam tinh dung dan - no chay o client, ai cung sua duoc.
 */
export function locGiaoDichMoi(txns, maDaCo) {
  const moi = [], daXuLy = [];
  // Trong cung MOT file cung co the co dong trung nhau, nen phai chan ca trong lo.
  const thay = new Set(maDaCo);
  for (const t of txns) {
    if (thay.has(t.ma_gd)) daXuLy.push(t);
    else { thay.add(t.ma_gd); moi.push(t); }
  }
  return { moi, daXuLy };
}

/**
 * Doc sao ke dinh dang CSV chuan hoa cua chinh minh.
 *
 * CHUA co parser ngan hang that: chua chon ngan hang, ma doan layout sao ke la viet code
 * khong chay duoc. Khi co sao ke that thi them parsers/<ngan-hang>.js tra ve dung kieu
 * GiaoDichTho[], phan con lai khong phai sua.
 *
 * Cot: ma_gd,ngay,so_tien,noi_dung
 */
export function docCsv(vanBan) {
  const dong = String(vanBan || '').trim().split(/\r?\n/);
  if (dong.length < 2) return [];
  const out = [];
  for (const d of dong.slice(1)) {
    const o = tachDongCsv(d);
    if (o.length < 4) continue;
    const so_tien = Number(String(o[2]).replace(/[^\d-]/g, ''));
    // Chi lay tien VAO. Sao ke co ca tien ra, cong nham vao la sai so.
    if (!Number.isFinite(so_tien) || so_tien <= 0) continue;
    out.push({ ma_gd: o[0].trim(), posted_at: o[1].trim(), so_tien, noi_dung: o[3] });
  }
  return out;
}

/** Tach mot dong CSV, hieu dau nhay kep va "" long nhau. */
function tachDongCsv(dong) {
  const o = [];
  let cur = '', trongNhay = false;
  for (let i = 0; i < dong.length; i++) {
    const c = dong[i];
    if (trongNhay) {
      if (c === '"' && dong[i + 1] === '"') { cur += '"'; i++; }
      else if (c === '"') trongNhay = false;
      else cur += c;
    } else if (c === '"') trongNhay = true;
    else if (c === ',') { o.push(cur); cur = ''; }
    else cur += c;
  }
  o.push(cur);
  return o;
}

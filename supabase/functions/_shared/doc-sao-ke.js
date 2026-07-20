// Doc sao ke cua BAT KY ngan hang nao bang cach anh xa cot.
//
// Vi sao khong viet parser rieng cho tung ngan hang: VNCLO lam vay va hardcode layout
// Vietcombank - doi ngan hang la hong, va khong ai biet no hong cho den luc doi soat.
// O day chi co MOT bo doc chung; su khac nhau giua cac ngan hang nam o mot ban ghi
// anh xa cot (cot nao la so tien, cot nao la noi dung...) do NGUOI chon tren giao dien
// va luu lai de lan sau tu dung.
//
// Luong: docBang() -> timDongTieuDe() -> doanAnhXa() -> nguoi sua neu doan sai
//        -> apDungAnhXa() -> GiaoDichTho[] chuan, tu day tro di doi-soat.js lo.

/** @typedef {{dongTieuDe:number, ma_gd:number|null, ngay:number, tien_vao:number,
 *             tien_ra:number|null, noi_dung:number}} AnhXaCot */

/** Bo dau tieng Viet + ha chu thuong, de so khop tieu de cot khong phu thuoc dau. */
export function boDau(s) {
  return String(s ?? '')
    // Khoang trong day la U+0300..U+036F (dau thanh tach ra sau khi normalize NFD).
    // Chung la ky tu KET HOP nen hien thi dinh vao dau ngoac vuong, trong nhu loi go -
    // dung xoa. Co test "boDau bo dau tieng Viet" giu cho khoi bi sua nham.
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/đ/g, 'd').replace(/Đ/g, 'D')
    .toLowerCase().trim();
}

/**
 * Doan dau phan cach cot: dau phay, cham phay hay tab.
 *
 * BAT BUOC phai doan, khong duoc coi ca ba deu la dau phan cach: sao ke dung dau cham
 * phay van co so tien viet "4,000,000", coi dau phay la phan cach thi mot o tien bi xe
 * thanh ba o va so tien 4 trieu doc ra thanh 4.
 *
 * Chi dem nhung dau nam NGOAI dau nhay kep, roi lay loai xuat hien nhieu nhat.
 */
export function doanDauPhanCach(vanBan) {
  const s = String(vanBan ?? '').replace(/\r\n?/g, '\n');
  const dem = { ',': 0, ';': 0, '\t': 0 };
  let trongNhay = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (c === '"') { trongNhay = !trongNhay; continue; }
    if (!trongNhay && c in dem) dem[c]++;
  }
  // Hoa thi uu tien dau phay: pho bien nhat, va la mac dinh khi file khong co dau nao.
  let tot = ',';
  for (const d of [';', '\t']) if (dem[d] > dem[tot]) tot = d;
  return tot;
}

/**
 * Tach CSV thanh luoi o. Hieu dau nhay kep, "" long nhau va xuong dong trong o.
 * Tu doan dau phan cach neu khong truyen vao.
 */
export function docBang(vanBan, dauPhanCach) {
  const luoi = [];
  const dpc = dauPhanCach || doanDauPhanCach(vanBan);
  let hang = [], o = '', trongNhay = false;
  const s = String(vanBan ?? '').replace(/\r\n?/g, '\n');
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (trongNhay) {
      if (c === '"' && s[i + 1] === '"') { o += '"'; i++; }
      else if (c === '"') trongNhay = false;
      else o += c;
    } else if (c === '"') trongNhay = true;
    else if (c === dpc) { hang.push(o); o = ''; }
    else if (c === '\n') { hang.push(o); luoi.push(hang); hang = []; o = ''; }
    else o += c;
  }
  if (o !== '' || hang.length) { hang.push(o); luoi.push(hang); }
  // CO Y giu ca hang rong thay vi loc di: loc thi chi so hang trong luoi lech khoi so
  // dong that trong file, va bao "bo hang 12" trong khi file cua nguoi ta hang 12 lai
  // la dong khac. Hang rong duoc bo qua o apDungAnhXa, khong tinh la giao dich bi mat.
  return luoi;
}

/** Hang khong co o nao co noi dung. */
const hangRong = (h) => !h || h.every((x) => String(x ?? '').trim() === '');

// Tu khoa nhan dang cot. Viet khong dau vi da qua boDau(). Xep tu CU THE den CHUNG
// CHUNG: "so tien ghi co" phai thang "so tien", neu khong cot ghi no cung khop.
const TU_KHOA = {
  ma_gd:    ['so tham chieu', 'so but toan', 'so chung tu', 'ma giao dich', 'ma gd',
             'reference', 'ref no', 'transaction id', 'so ct', 'trace'],
  ngay:     ['ngay giao dich', 'ngay hieu luc', 'ngay hach toan', 'transaction date',
             'posting date', 'value date', 'ngay', 'date'],
  // Bon tu cuoi la CHUNG CHUNG, cot y: nhieu sao ke chi co mot cot "Amount"/"So tien"
  // mang dau am duong thay vi tach ghi no / ghi co. Chung phai nam CUOI danh sach va
  // doanAnhXa phai tim tien_ra truoc, neu khong "So tien ghi no" cung khop "so tien"
  // va tien ra bi cong thanh tien vao.
  tien_vao: ['so tien ghi co', 'phat sinh co', 'ghi co', 'tien vao', 'credit',
             'amount in', 'deposit',
             'so tien giao dich', 'so tien', 'amount', 'gia tri'],
  tien_ra:  ['so tien ghi no', 'phat sinh no', 'ghi no', 'tien ra', 'debit',
             'amount out', 'withdrawal'],
  noi_dung: ['noi dung chi tiet', 'noi dung giao dich', 'noi dung', 'dien giai', 'mo ta',
             'transactions in detail', 'description', 'detail', 'remark', 'content'],
};

/**
 * Tim hang nao la tieu de.
 *
 * Sao ke ngan hang thuong co vai hang dau la ten chu tai khoan, so tai khoan, ky sao
 * ke... Lay bua hang 0 lam tieu de la sai. Tim hang khop duoc NHIEU tu khoa nhat.
 */
export function timDongTieuDe(luoi) {
  let tot = -1, diemTot = 0;
  const nhom = Object.values(TU_KHOA);
  // Chi quet 25 hang dau: tieu de khong bao gio nam sau do, va quet ca file thi gap
  // dong du lieu co chu "ngay" trong noi dung se doan nham.
  for (let i = 0; i < Math.min(luoi.length, 25); i++) {
    if (hangRong(luoi[i])) continue;
    const o = luoi[i].map(boDau);
    const diem = nhom.filter((tk) => o.some((x) => x && tk.some((t) => x.includes(t)))).length;
    if (diem > diemTot) { diemTot = diem; tot = i; }
  }
  // Duoi 2 nhom khop thi coi nhu khong nhan ra - de nguoi tu chon con hon doan bua.
  return diemTot >= 2 ? tot : -1;
}

/**
 * Doan anh xa cot tu hang tieu de. Doan sai khong sao: giao dien bay ra cho nguoi sua.
 * Tra ve cac chi so cot, null neu khong doan duoc.
 */
export function doanAnhXa(hangTieuDe) {
  const o = (hangTieuDe || []).map(boDau);
  const tim = (tuKhoa, daDung = []) => {
    for (const t of tuKhoa) {
      const i = o.findIndex((x, k) => x && x.includes(t) && !daDung.includes(k));
      if (i >= 0) return i;
    }
    return null;
  };
  // Tim tien_ra TRUOC tien_vao: nhieu sao ke co ca hai cot ten gan giong nhau
  // ("Ghi no" / "Ghi co"), tim "so tien" chung chung truoc la vo nham cot ghi no.
  const ma_gd    = tim(TU_KHOA.ma_gd);
  const ngay     = tim(TU_KHOA.ngay);
  const noi_dung = tim(TU_KHOA.noi_dung);
  const tien_ra  = tim(TU_KHOA.tien_ra, [ma_gd, ngay, noi_dung].filter((x) => x !== null));
  const tien_vao = tim(TU_KHOA.tien_vao,
    [ma_gd, ngay, noi_dung, tien_ra].filter((x) => x !== null));
  return { ma_gd, ngay, tien_vao, tien_ra, noi_dung };
}

/**
 * Doc so tien kieu Viet Nam.
 *
 * "4.000.000" va "4,000,000" deu la bon trieu. Quy tac: neu co CA hai loai dau phan
 * cach thi cai xuat hien SAU cung la dau thap phan. Neu chi co mot loai va no xuat
 * hien nhieu lan, do la dau ngan cach nghin. Neu xuat hien dung mot lan va theo sau
 * la 3 chu so, cung coi la ngan cach nghin - tien Viet gan nhu khong bao gio le
 * xu, con "1.234" thi chac chan la mot nghin hai tram ba muoi tu.
 */
export function docSoTien(s) {
  const goc = String(s ?? '').trim();
  // Tu choi thang chuoi hinh dang NGAY THANG. Neu chi boc het ky tu la roi doc so thi
  // "2026-07-03" thanh 20260703 va "03/07/2026" thanh 3072026 - anh xa nham cot Ngay
  // vao cot Tien vao se cho ra so tien hai muoi trieu ma khong bao loi gi.
  // Dau tru chi duoc phep o dau chuoi (so am).
  if (goc.includes('/')) return NaN;
  if (goc.lastIndexOf('-') > 0) return NaN;

  let t = goc.replace(/[^\d.,\-]/g, '');
  if (!t) return NaN;
  const am = t.startsWith('-');
  t = t.replace(/-/g, '');
  const cham = t.lastIndexOf('.'), phay = t.lastIndexOf(',');
  let nguyen = t, le = '';
  if (cham >= 0 && phay >= 0) {
    const cat = Math.max(cham, phay);
    nguyen = t.slice(0, cat); le = t.slice(cat + 1);
  } else if (cham >= 0 || phay >= 0) {
    const dau = cham >= 0 ? '.' : ',';
    const soLan = t.split(dau).length - 1;
    const duoi = t.slice(t.lastIndexOf(dau) + 1);
    if (soLan === 1 && duoi.length !== 3) { nguyen = t.slice(0, t.lastIndexOf(dau)); le = duoi; }
  }
  const so = Number(nguyen.replace(/[.,]/g, '') + (le ? '.' + le : ''));
  return Number.isFinite(so) ? (am ? -so : so) : NaN;
}

/**
 * Doc ngay. Nhan dd/mm/yyyy, dd-mm-yyyy, yyyy-mm-dd va co the kem gio.
 *
 * Uu tien NGAY TRUOC THANG khi mo ho: sao ke ngan hang Viet Nam dung dd/mm. Doan
 * nguoc lai thi 03/07 thanh mung 7 thang 3 - lech bon thang ma nhin khong ra.
 */
export function docNgay(s) {
  const t = String(s ?? '').trim();
  if (!t) return null;
  let m = t.match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})/);
  if (m) return chuanNgay(m[1], m[2], m[3], t);
  m = t.match(/^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})/);
  if (m) {
    const nam = m[3].length === 2 ? '20' + m[3] : m[3];
    return chuanNgay(nam, m[2], m[1], t);
  }
  const d = new Date(t);
  return isNaN(d) ? null : d.toISOString();
}

function chuanNgay(nam, thang, ngay, goc) {
  const gio = goc.match(/(\d{1,2}):(\d{2})(?::(\d{2}))?/);
  const p = (n) => String(n).padStart(2, '0');
  const d = new Date(Date.UTC(+nam, +thang - 1, +ngay,
    gio ? +gio[1] : 0, gio ? +gio[2] : 0, gio && gio[3] ? +gio[3] : 0));
  return isNaN(d) ? null : d.toISOString();
}

/**
 * Ap anh xa cot len luoi, tra ve giao dich TIEN VAO da chuan hoa.
 *
 * Tra ve ca danh sach dong bi bo va ly do: bo im lang thi mot cot anh xa sai se lam
 * mat sach giao dich ma khong ai biet, chi thay "0 giao dich" roi tuong thang do khong
 * ai chuyen tien.
 */
export function apDungAnhXa(luoi, anhXa) {
  const { dongTieuDe, ma_gd, ngay, tien_vao, tien_ra, noi_dung } = anhXa;
  const ra = [], bo = [];
  for (let i = dongTieuDe + 1; i < luoi.length; i++) {
    const h = luoi[i];
    // Hang rong khong phai giao dich bi mat, khong bao vao danh sach bo.
    if (hangRong(h)) continue;
    const lay = (k) => (k === null || k === undefined ? '' : (h[k] ?? ''));

    // Co cot ghi no rieng: hang nao co tien ra la hang chi, khong phai tien vao.
    if (tien_ra !== null && tien_ra !== undefined) {
      const raTien = docSoTien(lay(tien_ra));
      if (Number.isFinite(raTien) && raTien > 0) { bo.push({ hang: i + 1, ly_do: 'tien ra' }); continue; }
    }
    const soTien = docSoTien(lay(tien_vao));
    if (!Number.isFinite(soTien) || soTien <= 0) { bo.push({ hang: i + 1, ly_do: 'khong co tien vao' }); continue; }

    const ngayISO = docNgay(lay(ngay));
    if (!ngayISO) { bo.push({ hang: i + 1, ly_do: 'khong doc duoc ngay' }); continue; }

    const ma = String(lay(ma_gd)).trim();
    ra.push({
      ma_gd: ma,                       // rong = phia goi phai sinh ma thay the
      ma_la_thay_the: ma === '',
      posted_at: ngayISO,
      so_tien: Math.round(soTien),
      noi_dung: String(lay(noi_dung)).trim(),
    });
  }
  return { giao_dich: ra, bo };
}

/** Doc tu dau den cuoi voi anh xa tu doan. Nguoi khong sua gi thi dung duong nay. */
export function docTuDong(vanBan) {
  const luoi = docBang(vanBan);
  const dongTieuDe = timDongTieuDe(luoi);
  if (dongTieuDe < 0) return { luoi, dongTieuDe: -1, anhXa: null, giao_dich: [], bo: [] };
  const anhXa = { dongTieuDe, ...doanAnhXa(luoi[dongTieuDe]) };
  if (anhXa.ngay === null || anhXa.tien_vao === null || anhXa.noi_dung === null)
    return { luoi, dongTieuDe, anhXa, giao_dich: [], bo: [] };
  return { luoi, dongTieuDe, anhXa, ...apDungAnhXa(luoi, anhXa) };
}

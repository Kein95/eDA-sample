// Phần dùng chung của các bộ kiểm chạy trên trình duyệt thật.
//
// Vì sao phải là trình duyệt thật chứ không phải jsdom: trang tuyển sinh do support.js
// dựng ra và DỰNG LẠI mỗi lần đổi tab, trang quản trị thì phụ thuộc History API, CSP,
// và cách trình duyệt đọc <textarea>. Ba thứ đó chỉ đúng khi có một trình duyệt thật.
//
// Cần hai thứ chạy sẵn:
//   1. Máy chủ xem thử:  docker compose -f docker/docker-compose.yml up -d
//   2. Chrome mở cổng gỡ lỗi:
//        chrome --remote-debugging-port=9222 --user-data-dir=<thư mục tạm>
//
// Chạy:  node scripts/test-trinh-duyet-<ten>.mjs [địa chỉ gốc]
// Không truyền địa chỉ thì mặc định http://localhost:8791

export const CDP = 'http://127.0.0.1:9222';
export const GOC_MAC_DINH = 'http://localhost:8791';
export const cho = (ms) => new Promise((r) => setTimeout(r, ms));

/** Mở một tab mới và trả về bộ điều khiển. Tự gom lỗi console để kiểm sau. */
export async function mo(goc, duongDan) {
  let t;
  try {
    t = await (await fetch(`${CDP}/json/new?${encodeURIComponent(goc + duongDan)}`,
      { method: 'PUT' })).json();
  } catch (e) {
    console.error(`Không nối được Chrome ở ${CDP}. Mở Chrome với --remote-debugging-port=9222 rồi chạy lại.`);
    process.exit(2);
  }
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  let id = 0;
  const cho_hoi = new Map();
  const loi = [];
  const send = (m, p = {}) => new Promise((r) => {
    const i = ++id;
    cho_hoi.set(i, r);
    ws.send(JSON.stringify({ id: i, method: m, params: p }));
  });
  // Hai loi biet truoc, deu khong phai cua trang va khong sua duoc tu repo. De lai thi bo
  // kiem khong bao gio xanh duoc tren ban live, va mot bo kiem khong bao gio xanh thi som
  // muon cung bi tat. Danh sach nay phai NGAN va moi dong phai noi ro vi sao.
  const BO_QUA_LOI = [
    // Cloudflare tu chen beacon.min.js vao moi trang tren Pages; CSP cua trang chan no
    // dung nhu thiet ke.
    /static\.cloudflareinsights\.com/,
    // image-slot.js (component vendor, khong sua) tim mot tep trang thai KHONG bat buoc;
    // thieu thi no bo qua. Local khong thay loi nay vi nginx tra trang tuyen sinh kem ma
    // 200 cho moi duong dan la.
    /image-slots\.state\.json/,
  ];
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') {
      // Phai soi CA text lan url: loi tai tai nguyen chi ghi "Failed to load resource:
      // ... 404 ()" trong text, dia chi nam rieng o truong url. Loc theo moi text thi
      // khong bao gio khop, ma cung khong ai biet la khong khop.
      const e2 = m.params.entry;
      const cho_qua = BO_QUA_LOI.some((re) => re.test(e2.text) || re.test(e2.url || ''));
      if (!cho_qua) loi.push(`${e2.text.slice(0, 120)}${e2.url ? ' <- ' + e2.url : ''}`);
    }
    if (m.id && cho_hoi.has(m.id)) { cho_hoi.get(m.id)(m.result); cho_hoi.delete(m.id); }
  };
  await new Promise((r) => { ws.onopen = r; });
  await send('Runtime.enable');
  await send('Log.enable');
  await send('Page.enable');
  await send('Network.enable');
  // Tat cache: dang do chinh file vua sua, doc phai ban cu la ket luan sai.
  await send('Network.setCacheDisabled', { cacheDisabled: true });

  const js = async (bieuThuc) => (await send('Runtime.evaluate',
    { expression: bieuThuc, returnByValue: true, awaitPromise: true })).result.value;

  return {
    js, send, loi,
    /** Đợi tới khi biểu thức trả về giá trị đúng, hoặc hết giờ. */
    async doi(bieuThuc, giay = 20) {
      for (let i = 0; i < giay * 4; i++) {
        if (await js(bieuThuc)) return true;
        await cho(250);
      }
      return false;
    },
    async dong() { await fetch(`${CDP}/json/close/${t.id}`); ws.close(); },
  };
}

/** Bộ đếm kết quả. Giữ ngoài để nhiều nhóm kiểm cùng cộng dồn vào một chỗ. */
export function boDem() {
  let hong = 0;
  return {
    dat(ok, ten) {
      console.log(`  ${ok ? 'ok  ' : 'HONG'} ${ten}`);
      if (!ok) hong++;
    },
    nhom(ten) { console.log(`\n=== ${ten}`); },
    ketThuc(tongKet) {
      console.log(hong ? `\n${hong} kiem tra HONG` : `\n${tongKet}`);
      // Đợi socket đóng hẳn rồi mới thoát, tránh nổ libuv trên Windows.
      setTimeout(() => process.exit(hong ? 1 : 0), 200);
    },
  };
}

export const goc = () => process.argv[2] || GOC_MAC_DINH;

# eDA 2026 · Trang tuyển sinh End2End Data Analytics

### 🔗 Xem trang chạy thật

| | |
|---|---|
| Trang tuyển sinh | **https://eda.luonvuituoi.work** |
| Xem thử trang quản trị | **https://eda.luonvuituoi.work/dashboard** |
| Trang quản trị (màn đăng nhập) | **https://eda.luonvuituoi.work/admin** |

> ### ⚠️ Đây là bản demo ý tưởng
>
> **Khoá học là có thật.** Nội dung lấy từ
> [tài liệu gốc của khoá](https://drive.google.com/drive/folders/1JlXxhr-m3yKF8m8oZxoSg5hcq77CwNMh).
>
> Nhưng **trang này** chỉ là bản phác thảo giao diện, **không phải trang tuyển sinh chính
> thức** và **chưa liên kết với AI VIETNAM**. **Form đăng ký không hoạt động** (Supabase
> chưa dựng, xem phần B4), điền vào sẽ báo lỗi chứ không báo thành công giả. Muốn đăng ký
> thật thì liên hệ trực tiếp AI VIETNAM.

Khai giảng 06.09.2026, kết thúc 05.2027. 8 module, 9 domain, 100 buổi live online.

---

## Bạn đang cần gì?

| Việc bạn định làm | Đọc phần nào |
|---|---|
| Dùng trang quản trị hằng ngày: xem đăng ký, đối soát tiền, sửa chữ trên trang | **[Phần A](#phần-a--dành-cho-người-vận-hành)**, không cần biết lập trình |
| Chạy trang trên máy mình, sửa code, đưa lên mạng | **[Phần B](#phần-b--dành-cho-người-kỹ-thuật)** |

---

# PHẦN A · Dành cho người vận hành

Phần này viết cho người **không cần biết lập trình**. Chỉ cần trình duyệt.

## A1. Vào trang quản trị

Có hai cửa vào, **cùng một trang**:

| Địa chỉ | Dùng khi nào |
|---|---|
| `eda.luonvuituoi.work/dashboard` | **Xem thử.** Vào thẳng, không cần mật khẩu. Dữ liệu là 10 đăng ký demo, không phải người thật. |
| `eda.luonvuituoi.work/admin` | **Dùng thật.** Có màn đăng nhập. Chỉ chạy được sau khi kỹ thuật đã dựng xong Supabase (phần B4). |

Số điện thoại trong bản demo đều thuộc dải `0900 0000 xx` (Việt Nam không cấp phát dải
này) và email dùng `example.com`, nên **không thể trùng người thật**.

Mỗi tab có địa chỉ riêng, lưu vào dấu trang được, gửi cho đồng nghiệp cũng mở đúng chỗ:

| Tab | Địa chỉ |
|---|---|
| Đăng ký | `/dashboard/list` |
| Đối soát | `/dashboard/payments` |
| Nội dung trang | `/dashboard/web` |
| Tài khoản | `/dashboard/users` |
| Nhật ký | `/dashboard/log` |

## A2. Năm tab dùng để làm gì

| Tab | Việc |
|---|---|
| **Đăng ký** | Danh sách người đăng ký. Lọc theo khoảng ngày, tìm theo tên hoặc mã, tải CSV. |
| **Đối soát** | Đưa file sao kê ngân hàng vào, máy tự khớp giao dịch với người đăng ký, bạn tick xác nhận đã thu. |
| **Nội dung trang** | Sửa chữ và số trên trang tuyển sinh mà không cần đụng code. |
| **Tài khoản** | Xem ai đang có quyền gì, đổi vai. |
| **Nhật ký** | Mọi thao tác ai làm lúc nào, tải về CSV hoặc TXT. |

## A3. Ba vai, ai làm được gì

| Việc | Trợ giảng | Kế toán | Quản trị |
|---|:---:|:---:|:---:|
| Xem danh sách học viên | ✅ | ✅ | ✅ |
| Xem số điện thoại phụ huynh | ❌ | ✅ | ✅ |
| Xem số tiền, giao dịch | ❌ | ✅ | ✅ |
| Tải sao kê, khớp, xác nhận đã thu | ❌ | ✅ | ✅ |
| Miễn giảm, đổi số phải đóng | ❌ | ❌ | ✅ |
| Sửa thông tin đăng ký | ❌ | ❌ | ✅ |
| Sửa chữ trên trang tuyển sinh | ❌ | ❌ | ✅ |
| Cấp quyền cho tài khoản khác | ❌ | ❌ | ✅ |
| Xem nhật ký | ❌ | ❌ | ✅ |

Tab nào vai đó không được dùng thì **không hiện ra**, khỏi bấm nhầm.

> **Vì sao kế toán không được miễn giảm.** Kế toán ghi nhận **tiền vào**, quản trị quyết
> định **phải thu bao nhiêu**. Một tài khoản làm được cả hai thì miễn giảm khống rồi khớp
> cho khớp sổ là thao tác không ai phát hiện được. Đây là lý do duy nhất, không phải vì
> không tin ai.

Ở bản demo (`/dashboard`) có ô **"xem như:"** trên thanh tiêu đề để thử xem mỗi vai nhìn
thấy gì. Bản thật không có ô này: vai đến từ tài khoản đăng nhập.

## A4. Việc thường làm

### A4.1 Xem và lọc danh sách đăng ký

Tab **Đăng ký**. Có sẵn 4 mốc nhanh (hôm nay, 7 ngày, 30 ngày, tất cả) và hai ô chọn
ngày để tự đặt khoảng bất kỳ. Ô tìm kiếm dò theo tên, mã, số điện thoại.

Nút **Tải CSV** xuất đúng phần đang hiện trên màn hình. Mở bằng Excel được luôn.

### A4.2 Đối soát tiền

Tab **Đối soát**. Bốn bước:

1. **Bấm "Chọn file sao kê…"** rồi chọn file tải từ ngân hàng. Nhận `.xls`, `.xlsx`,
   `.csv` của **bất kỳ ngân hàng nào**. Tên cột, thứ tự cột, mấy dòng thừa ở đầu file,
   ngày kiểu `dd/mm/yyyy` hay kiểu khác, tất cả đều tự nhận.

2. **Kiểm bảng "Cột nào là gì".** Máy đoán cột nào là ngày, cột nào là số tiền, cột nào
   là nội dung chuyển khoản. Đoán sai thì chọn lại, bấm **"Đọc lại theo cột đã chọn"**.
   Lần sau mở sao kê cùng ngân hàng nó tự nhớ.

3. **Xem ba nhóm kết quả:**
   - **Đã khớp**: nhận ra người nộp. Dòng nào khớp bằng **mã đăng ký** thì đã tick sẵn.
     Dòng khớp bằng **số điện thoại** thì **không** tick sẵn, phải tự nhìn rồi tick, vì
     số điện thoại có thể là người nhà nộp hộ.
   - **Chưa khớp**: không nhận ra ai. Cột "Lý do" nói vì sao.
   - **Đã xác nhận, đã vào sổ**: nộp lại đúng file cũ thì các dòng này nằm ở đây chứ
     không cộng tiền lần thứ hai.

4. **Bấm "Xác nhận đã thu"**. Chỉ những dòng đang tick mới được ghi.

> **Nộp trùng file không sao.** Mỗi giao dịch có mã riêng của ngân hàng, đã vào sổ rồi thì
> lần sau bị nhận ra ngay. Cứ nộp lại nếu không nhớ đã nộp chưa.

### A4.3 Sửa chữ trên trang tuyển sinh

Tab **Nội dung trang**. Chỉ vai **quản trị** sửa được, vai khác chỉ xem.

Trang tuyển sinh có hơn 600 câu chữ, gom sẵn theo đúng 5 tab của trang. Có ô **Tìm chữ**
ở trên, gõ vài chữ trong câu cần sửa là ra.

| Nút | Làm gì |
|---|---|
| **Lưu nháp** | Cất lại, **khách chưa thấy gì**. |
| **Xem thử trên trang** | Mở trang tuyển sinh với bản nháp, chỉ mình bạn thấy. |
| **Xuất bản** | Đẩy lên trang thật, từ lúc này khách thấy. |
| **Hoàn về mặc định** | Bỏ hết mọi sửa đổi, trả về chữ gốc. |
| **Đọc lại trang** | Quét lại danh sách chữ. Thường không cần bấm, máy tự quét lại khi trang đổi. |

Nhóm **"Giá trị lặp nhiều nơi"** ở trên cùng là những thứ xuất hiện ở nhiều chỗ:
ngày khai giảng nằm ở **12 chỗ** trong trang, sửa một lần là đổi hết cả 12, không sót.

**Không thêm hay bớt khối được**, chỉ sửa chữ có sẵn. Trang này căn tay rất kỹ (vòng tròn
4 phần, dải 8 module, quả địa cầu), cho thêm khối tuỳ ý là mọi lần sửa đều có thể phá bố
cục. Cần thêm mục mới thì nhờ kỹ thuật.

Gõ thẻ HTML (kiểu `<b>đậm</b>`) sẽ hiện ra nguyên văn chứ không thành chữ đậm. Cố ý như
vậy để không ai chèn được mã lạ vào trang công khai.

### A4.4 Cấp quyền cho người mới

Tab **Tài khoản**. Đổi vai bằng ô chọn ở cột cuối, đổi xong có hiệu lực ngay.

**Tạo tài khoản mới và xoá tài khoản không làm ở đây.** Việc đó nhờ kỹ thuật làm trong
bảng điều khiển Supabase. Lý do: nếu để chức năng tạo tài khoản nằm trong trình duyệt thì
bất kỳ ai mở được trang cũng tự cấp quyền quản trị cho mình.

Người vừa được đổi vai phải **đăng xuất rồi đăng nhập lại** thì quyền mới có tác dụng.

### A4.5 Xem và tải nhật ký

Tab **Nhật ký**. Mọi thao tác đều được ghi: ai, lúc nào, làm gì, chi tiết ra sao. Lọc
theo người, theo loại thao tác, hoặc gõ từ khoá.

| Nút | Khi nào dùng |
|---|---|
| **Tải CSV** | Cần **sắp xếp, lọc, thống kê** trong Excel hoặc Google Sheets. |
| **Tải TXT** | Cần **đọc bằng mắt** hoặc gửi kèm email. Mở bằng Notepad là thấy ngay. |

Cả hai đều xuất **đúng phần đang lọc**, không phải cả sổ. Bản TXT ghi rõ ở đầu file là
đang lọc theo gì.

> Hai định dạng **nặng gần như nhau** (đo 200 dòng: TXT bằng 98% CSV). Chọn theo việc bạn
> định làm với nó, không phải theo dung lượng.

**Không ai xoá hay sửa được nhật ký, kể cả quản trị.** Một cuốn sổ sửa được thì không còn
là bằng chứng, mà giá trị duy nhất của nó là làm bằng chứng.

## A5. Những việc KHÔNG làm ở trang quản trị

| Việc | Nhờ ai |
|---|---|
| Tạo hoặc xoá tài khoản | Kỹ thuật (bảng điều khiển Supabase) |
| Thêm mục mới, đổi bố cục trang tuyển sinh | Kỹ thuật |
| Đổi học phí, đổi số đợt đóng | Kỹ thuật (nằm trong cơ sở dữ liệu) |
| Xoá dữ liệu người đăng ký | Kỹ thuật, và nhớ đây là dữ liệu cá nhân của trẻ vị thành niên |

## A6. Gặp sự cố

| Hiện tượng | Làm gì |
|---|---|
| Đăng nhập được nhưng bảng trống trơn | Tài khoản chưa được cấp vai. Nhờ kỹ thuật chạy bước B4.5. |
| Vừa được cấp quyền mà vẫn không thấy gì | Đăng xuất rồi đăng nhập lại. |
| Sửa chữ, bấm Xuất bản mà trang không đổi | Bấm Ctrl+F5 trên trang tuyển sinh để tải lại không dùng bản nhớ. |
| Sao kê đọc ra sai số tiền | Sai cột. Vào bảng "Cột nào là gì" chọn lại rồi bấm "Đọc lại theo cột đã chọn". |
| Trang báo lỗi đỏ | Chụp màn hình cả dòng chữ đỏ rồi gửi kỹ thuật. Đừng bấm lại nhiều lần. |

---

# PHẦN B · Dành cho người kỹ thuật

```
┌─ Trình duyệt ────────────┐      ┌─ Supabase ──────────────────────────┐
│ TuyenSinh-eDA2026.dc.html│─POST→│ edge function  eda-register         │
│  (trang tuyển sinh)      │      │   ↓ service-role key                │
│                          │      │ bảng  public.eda_registration (RLS) │
│ admin.html               │←GET──│   ↑ PostgREST + Realtime            │
│  (quản trị, 5 tab)       │      │     phân quyền theo 3 vai           │
└──────────────────────────┘      └─────────────────────────────────────┘
```

`/dashboard` và `/admin` là **cùng một file** `admin.html`, khác nhau ở điểm vào.
Cloudflare Pages cắt đuôi `.html`, nên `/admin.html` bị chuyển hướng sang `/admin`.

## B1. Chạy thử tại máy

Trang là file tĩnh, nhưng **không mở trực tiếp bằng `file://` được**: mỗi tab là một
đường dẫn thật (`/pathway`, `/dashboard/web`…) nên cần một web server biết rewrite.

### Cách nhanh nhất (Docker)

```bash
cd docker
docker compose up -d
```

Mở http://localhost:8791

Dừng: `docker compose down`. Cấu hình ở `docker/nginx-eda.conf`, thư mục gốc repo được
gắn vào read-only nên sửa file là F5 thấy ngay.

> Cổng chỉ mở cho chính máy này (`127.0.0.1:8791`), không ra mạng LAN. Web root là **cả
> thư mục repo**, nghĩa là `/supabase/migrations/*.sql`, `/data/eDA_v9.xlsx` và `/.git`
> đều tải về được. Ở nhà thì không sao, ở quán cà phê hay mạng công ty thì ai cũng xem
> được. Cần máy khác trong mạng xem thì sửa lại thành `"8791:80"` trong
> `docker/docker-compose.yml`, và nhớ sửa về sau khi xong.

Máy chủ này **rộng rãi hơn bản live**: mọi đường dẫn sai đều trả trang tuyển sinh với mã
200, nên link gãy không lộ ra. Bản Cloudflare Pages sẽ trả 404. Trước khi tin là xong,
kiểm bằng `node scripts/dung-thu-muc-xuat-ban.mjs`, script đó đối chiếu mọi `src=`,
`href=`, `import` của hai trang với danh sách file được deploy.

> **Đừng chạy `docker compose down --remove-orphans` trong thư mục này.** Máy đang có
> stack khác dùng chung Docker; cờ đó sẽ xoá luôn container của stack kia.

### Không có Docker

Cần server có URL rewrite. `python -m http.server` **không dùng được** (không rewrite).
Dùng `npx serve` với cấu hình rewrite, hoặc cài nginx và chép `docker/nginx-eda.conf`.

### Kiểm tra sau khi chạy

| Việc | Kỳ vọng |
|---|---|
| Mở `/` | Tab Tổng quan |
| Mở thẳng `/pathway` rồi F5 | Tab Lộ trình học, **không 404** |
| Mở thẳng `/dashboard/web` rồi F5 | Trang quản trị, tab Nội dung trang, **không phải trang tuyển sinh** |
| Bấm qua lại các tab | URL đổi theo, nút Back trình duyệt chạy đúng |
### Các bộ kiểm tra

Chạy được ngay, không cần gì thêm:

```bash
node scripts/test-bao-mat.mjs      # 20 kiểm tra: CSP, SRI, rò rỉ khoá
node scripts/test-doi-soat.mjs     # 22 kiểm tra: khớp giao dịch với người đăng ký
node scripts/test-doc-sao-ke.mjs   # 32 kiểm tra: đọc sao kê của ngân hàng bất kỳ
node scripts/dung-thu-muc-xuat-ban.mjs   # dựng bản deploy, báo lỗi nếu thiếu file
```

Cần Docker đang chạy:

```bash
bash scripts/test-db.sh            # 60 kiểm tra: dựng Postgres sạch, chạy migration
                                   # thật, giả lập đăng nhập từng vai rồi gọi thật
```

Cần thêm một Chrome mở cổng gỡ lỗi:

```bash
chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-eda
node scripts/test-trinh-duyet-duong-dan-vai.mjs   # 22 kiểm tra: URL từng tab, F5, Back, ba vai
node scripts/test-trinh-duyet-noi-dung.mjs        # 15 kiểm tra: sửa chữ, đếm trên cả 6 tab
node scripts/test-trinh-duyet-nhat-ky.mjs         # 16 kiểm tra: xuất CSV/TXT, phạm vi lọc
```

Ba bộ cuối chạy trên trình duyệt thật vì trang tuyển sinh do `support.js` dựng lại mỗi
lần đổi tab, và vì History API, CSP, cách trình duyệt đọc `<textarea>` chỉ đúng khi có
trình duyệt thật. Chúng đã bắt được lỗi mà đọc code không thấy: cả trang chết trắng ở
đường dẫn con, ô chọn vai hiện sai vai, `<input>` nuốt ngắt dòng.

## B2. Cấu trúc thư mục

| Đường dẫn | Là gì |
|---|---|
| `TuyenSinh-eDA2026.dc.html` | **Toàn bộ trang tuyển sinh**, một file duy nhất (~250KB) |
| `admin.html` | Trang quản trị, 5 tab, phân quyền theo vai |
| `support.js` | Runtime DesignCombo cho `.dc.html` (không sửa) |
| `image-slot.js` | Web component khung ảnh (không sửa) |
| `globe.html` | Quả địa cầu, nhúng bằng iframe vào trang chính |
| `map-vietnam.html` | Bản đồ Việt Nam (hiện chưa dùng) |
| `assets/` | Logo, hoạ tiết trống đồng, ảnh thumbnail video |
| `ava/` | Ảnh 4 giảng viên. `crop-*.jpg` là bản đang dùng |
| `data/` | File nguồn: `eDA_v9.xlsx` (giáo trình), sơ đồ drawio, ghi chú |
| `docker/` | nginx + compose để chạy thử |
| `docs/` | Tài liệu dự án, quan trọng nhất là `deployment-guide.md` |
| `scripts/` | Script sinh nội dung từ Excel, và các bộ kiểm tra |
| `supabase/` | Migration SQL, edge function, và **logic khớp giao dịch dùng chung** |
| `_redirects`, `_headers` | Cấu hình Cloudflare Pages |

### Logic dùng chung giữa trình duyệt, edge function và test

`supabase/functions/_shared/doi-soat.js` và `doc-sao-ke.js` được **cả ba nơi** nạp: trang
quản trị (qua `<script type="module">`), edge function, và `scripts/test-*.mjs`. Chép tay
ra bản thứ hai thì bản demo sẽ trôi khác bản thật lúc nào không biết, và test sẽ test
nhầm bản không ai chạy.

Vì vậy `admin.html` import bằng **đường dẫn từ gốc** (`/supabase/...`) chứ không phải
`./supabase/...`: ở `/dashboard/web` thì `./` tính từ `/dashboard/` và đi tìm sai chỗ,
mà đường dẫn sai đó lại khớp luật rewrite nên máy chủ trả HTML thay vì JS, trình duyệt từ
chối module sai MIME và **cả trang chết trắng**.

### Về file `.dc.html`

Định dạng **DesignCombo**: HTML thường cộng runtime phản ứng trong `support.js`.

| Cú pháp | Nghĩa |
|---|---|
| `{{ bien }}` | Chèn giá trị từ state |
| `<sc-if value="{{ dk }}">` | Hiện khối khi điều kiện đúng |
| `<sc-for>` | Lặp danh sách |
| `<helmet>` | Nội dung đẩy vào `<head>` |
| `<x-import>` | Nhúng web component |
| `class Component extends DCLogic` | Khối logic cuối file, có `state` và `renderVals()` |

Trang có 6 tab, mỗi tab một đường dẫn, bảng ánh xạ ở hằng `TAB_SLUGS`:

```js
const TAB_SLUGS = ['', 'pathway', 'early', 'docs', 'mentors', 'register'];
```

Trang quản trị có bảng tương tự tên là `SLUG` trong `admin.html`. Đổi slug thì phải sửa
cả `_redirects`, `docker/nginx-eda.conf` và `docs/deployment-guide.md`.

**support.js dựng lại DOM mỗi lần đổi tab.** Bất cứ thứ gì chèn vào trang bằng JavaScript
đều bị ghi đè ở lần dựng kế tiếp, nên phần áp nội dung sửa được dùng `MutationObserver`
để áp lại.

## B3. Sinh lại nội dung từ file nguồn

Một số phần **không gõ tay** mà sinh từ `data/eDA_v9.xlsx`:

```bash
python scripts/build-domain-matrix.py     # bảng 10 ngành × 10 mảng phân tích
python scripts/build-overview-diagram.py  # sơ đồ tổng quan
python scripts/build-syllabus-html.py     # lịch chi tiết từng module
```

Script tự tìm khối đã chèn lần trước bằng comment mốc và thay đúng khối đó, nên chạy lại
nhiều lần được, không sinh trùng.

> `scripts/` còn khoảng 40 file `fix_*.py`, `update_*.py` là script dùng một lần trong
> quá trình làm. Không cần chạy lại. Giữ để tra cứu lịch sử chỉnh sửa.

## B4. Dựng backend

**Chưa làm bước này thì form đăng ký không lưu được gì** và trang quản trị chỉ chạy ở chế
độ demo. Chi tiết đầy đủ ở [`docs/deployment-guide.md`](docs/deployment-guide.md).

### B4.1 Tạo project Supabase

Dùng **project riêng cho eDA**, đừng ghép chung dự án khác: bảng đăng ký chứa số điện
thoại phụ huynh của trẻ vị thành niên, tách riêng thì phân quyền và xoá dữ liệu sau này
đều gọn.

Ghi lại `Project URL` và `anon key` ở Settings → API.

### B4.2 Chạy migration

SQL Editor, chạy lần lượt **8 file** trong `supabase/migrations/` theo đúng thứ tự số.

| File | Thêm gì |
|---|---|
| `0001`–`0004` | Bảng đăng ký, RLS, chống spam |
| `0005` | Phương án học phí, các đợt đóng |
| `0006` | Giao dịch ngân hàng, nhật ký `eda_audit` |
| `0007` | Ba vai, quyền theo cột, cổng chặn trong view, quyền đọc nhật ký |
| `0008` | Nội dung trang sửa được |

Sau khi chạy xong, **kiểm hai thứ trong Supabase**:

1. **Authentication → Providers → Email → tắt "Enable Sign Ups"** nếu không dùng. Để mở
   thì bất kỳ ai cũng tự tạo được tài khoản và trở thành `authenticated`. Các policy đã
   đổi sang kiểm **vai** thay vì kiểm "đã đăng nhập" nên tài khoản tự tạo không có vai sẽ
   không đọc được gì, nhưng tắt hẳn vẫn gọn hơn.
2. `service_role key` chưa từng xuất hiện trong repo: `git log -p | grep -i service_role`

Muốn kiểm trước khi chạy lên Supabase thật: `bash scripts/test-db.sh` dựng một Postgres
sạch trong Docker, chạy đúng 8 file đó rồi kiểm phân quyền bằng cách **giả lập đăng nhập
từng vai và gọi thật**.

### B4.3 Deploy edge function

```bash
npx supabase login
npx supabase link --project-ref <ref-cua-ban>
npx supabase functions deploy eda-register --no-verify-jwt
```

Rồi đặt biến môi trường ở Settings → Edge Functions → Secrets. **Bắt buộc** là
`EDA_ALLOWED_ORIGINS`.

### B4.4 Điền các chỗ `REPLACE-ME`

```bash
grep -rn "REPLACE-ME" TuyenSinh-eDA2026.dc.html admin.html
```

| File | Cần điền |
|---|---|
| `TuyenSinh-eDA2026.dc.html` | `EDA_REGISTER_ENDPOINT` |
| `admin.html` | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, **và 2 URL trong thẻ CSP** |

Quên CSP là đăng nhập admin bị trình duyệt chặn mà không rõ lý do.

`anon key` là khoá công khai theo thiết kế, lộ không sao. Thứ chặn truy cập là RLS.
**Tuyệt đối không** đưa `service_role key` vào bất kỳ file nào trong repo.

### B4.5 Tạo tài khoản quản trị

Authentication → Users → Add user. Đặt mật khẩu ngẫu nhiên **ngay trong màn hình đó**,
lưu vào trình quản lý mật khẩu. Không ghi vào repo, không gửi qua chat.

Rồi cấp vai trong SQL Editor:

```sql
update auth.users
   set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb)
                           || '{"role":"EDA_ADMIN"}'::jsonb
 where email = 'admin@aivietnam.edu.vn';
```

Vai hợp lệ: `EDA_TA` (trợ giảng), `EDA_ACCOUNTANT` (kế toán), `EDA_ADMIN` (quản trị).

Tài khoản phải **đăng xuất rồi đăng nhập lại** thì token mới mang vai. Thiếu bước này thì
đăng nhập vẫn được nhưng bảng trống trơn.

> Đừng dùng số hotline làm mật khẩu. Số `0911 118 758` đang in công khai ở chân trang.

### B4.6 Bật rewrite trên host

| Host | Cấu hình |
|---|---|
| nginx | xem `docker/nginx-eda.conf` |
| Vercel | `vercel.json` với rewrite về `/TuyenSinh-eDA2026.dc.html` |
| Cloudflare Pages | file `_redirects`, có sẵn trong repo |

Thiếu bước này thì bấm tab vẫn chạy, nhưng F5 hoặc mở link chia sẻ sẽ 404.

Phải phủ **cả đường dẫn con của trang quản trị** (`/dashboard/*`, `/admin/*`), không chỉ
`/dashboard`. Thiếu thì F5 tại `/dashboard/web` ra trang tuyển sinh và trả **mã 200**,
nên nhìn qua tưởng không sao.

## B5. Đưa lên Cloudflare Pages

```bash
node scripts/dung-thu-muc-xuat-ban.mjs
npx wrangler pages deploy .xuat-ban --project-name eda --branch master
```

**Phải deploy từ `.xuat-ban`, đừng deploy từ thư mục gốc.** `wrangler pages deploy` không
đọc `.gitignore` (cũng không đọc `.assetsignore`), nên deploy từ gốc là `data/eDA_v9.xlsx`,
toàn bộ migration SQL và tài liệu PDF đều thành URL công khai. Script trên chép ra đúng
20 file trang thật sự cần, khoảng 1.2MB, và **báo lỗi nếu `admin.html` import một file
không có trong danh sách**.

Hai điểm khác nginx, đã ghi trong `_redirects`:

- Pages **tự cắt đuôi `.html`**, nên đích phải là `/TuyenSinh-eDA2026.dc` không kèm
  `.html`, nếu không Pages trả 308 và mọi tab bị dồn về một địa chỉ.
- **Đừng dùng luật `/*` ở gốc.** Trên Pages nó nuốt cả file có thật, `support.js` và ảnh
  đều bị trả về HTML. Luật `/dashboard/*` thì an toàn vì dưới thư mục đó không có file
  thật nào.

`_headers` phải lặp lại khối `frame-ancestors` cho **mọi** đường dẫn tới trang quản trị:
Pages khớp `_headers` theo đường dẫn **người dùng gọi**, không theo file đích.

## B6. Bảo mật

| Lớp | Chặn gì |
|---|---|
| RLS trên mọi bảng | Người lạ đọc dữ liệu |
| Mệnh đề `where` **trong view** | View chạy bằng quyền người tạo nên **bỏ qua RLS**. Bảng gốc kín không có nghĩa là view kín. |
| Kiểm vai **trong thân hàm** `security definer` | Hàm loại này bỏ qua RLS, và PostgREST bày mọi hàm thành một endpoint `/rpc/…` |
| Quyền theo cột | Kế toán sửa số tiền của giao dịch |
| Ràng buộc `xac_nhan_boi` ở **cả INSERT lẫn UPDATE** | Chèn thẳng một dòng đã đánh dấu "người khác đã duyệt" |
| Che thông tin cá nhân khi ghi nhật ký | Nhật ký không có hạn lưu, ghi nguyên bản ghi vào là biến chính sách xoá sau 24 tháng thành di dời |
| `revoke … truncate` | RLS không áp cho `TRUNCATE`, và `revoke delete` không bao gồm nó |
| CSP trong `<meta>` | Script lạ, kết nối ra ngoài Supabase |
| `frame-ancestors` trong `_headers` | Nhúng trang quản trị vào iframe để lừa bấm |
| SRI trên script CDN | CDN bị đổi nội dung |
| Lọc thẻ lúc **ghi** | Người trong nhà chèn HTML vào trang công khai |
| Chặn công thức khi xuất CSV | Ô bắt đầu bằng `=` `+` `-` `@` chạy như công thức khi mở Excel |

`node scripts/test-bao-mat.mjs` kiểm 20 điểm phía trình duyệt, `bash scripts/test-db.sh`
kiểm 60 điểm phía cơ sở dữ liệu bằng cách **giả lập đăng nhập từng vai rồi gọi thật**.

> **Kiểm cả cửa còn lại, đừng chỉ kiểm cửa đã che.** Bộ kiểm bản trước chứng minh rằng
> view của trợ giảng không có cột SĐT phụ huynh, rồi kết luận là kín. Nhưng bảng gốc vẫn
> mở: trợ giảng gọi thẳng `GET /rest/v1/eda_registration?select=guardian_phone` là lấy
> được. Che một cửa mà không kiểm cửa kia thì bộ kiểm chỉ chứng minh được rằng cửa đã che
> thì đã che.

### Trước khi nối Supabase thật, phải làm

Bản demo cố ý mở cửa cho ai cũng vào xem. Nối dữ liệu thật vào mà quên đóng thì cửa vẫn mở.

| # | Việc | Ở đâu | Không làm thì sao |
|---|---|---|---|
| 1 | Bỏ dòng `/dashboard` | `_redirects` (giữ `/admin` và `/admin/*`) | Ai cũng vào thẳng trang quản trị, không cần mật khẩu |
| 2 | Bỏ link `/dashboard` trong banner cảnh báo | `admin.html`, khối `#demoBanner` | Trang tự chỉ đường vào cửa đang mở |
| 3 | Bỏ `'admin.html'` khỏi danh sách deploy | `scripts/dung-thu-muc-xuat-ban.mjs` | Trang quản trị nằm ở URL đoán được. Bỏ thì phải deploy nó riêng, hoặc chấp nhận rằng RLS mới là thứ chặn chứ không phải URL |
| 4 | Tắt **Enable Sign Ups** | Supabase → Authentication → Providers → Email | Ai cũng tự tạo được tài khoản. Các policy đã kiểm *vai* nên tài khoản không vai đọc không được gì, nhưng tắt hẳn vẫn gọn hơn |
| 5 | Kiểm `service_role key` chưa từng lọt vào repo | `git log -p \| grep -i service_role` | Khoá đó bỏ qua toàn bộ RLS. Lọt rồi thì phải xoay khoá, không phải xoá commit |

Kiểm lại sau khi làm xong: mở `https://<tên miền>/dashboard` ở cửa sổ ẩn danh. Phải ra 404
hoặc màn đăng nhập, không được ra bảng dữ liệu.

## B7. Việc còn phải làm, và làm thế nào

Bốn việc dưới đây chưa làm vì **chưa có project Supabase thật**, không phải vì khó. Mỗi
việc đều ghi đủ để người tiếp nhận làm được mà không cần hỏi lại.

### B7.1 Hai edge function đối soát

Logic khớp giao dịch đã xong và đã kiểm 22 phép ở `supabase/functions/_shared/doi-soat.js`.
Còn thiếu tầng HTTP bọc quanh nó.

| Function | Nhận gì | Làm gì |
|---|---|---|
| `eda-doi-soat` | File sao kê (`multipart/form-data`) | Đọc file, khớp với người đăng ký, ghi vào `eda_bank_txn` với `xac_nhan_luc = null`, trả về ba nhóm kết quả |
| `eda-xac-nhan-gd` | Mảng `id` giao dịch | Đặt `xac_nhan_luc = now()`, `xac_nhan_boi = auth.uid()` cho những dòng được chọn |

Ba điều bắt buộc, thiếu là hỏng:

1. **Đọc file ở edge function, không đọc trong trình duyệt.** Bản demo đọc trong trình
   duyệt để chạy được mà không cần máy chủ. Bản thật thì máy chủ phải là nơi quyết định:
   trình duyệt gửi lên con số nào cũng được nếu tin nó.
2. **Dùng chung `_shared/doi-soat.js`**, đừng chép ra bản thứ hai. Chép rồi thì bản demo và
   bản thật trôi khác nhau lúc nào không biết, và bộ kiểm sẽ kiểm bản không ai chạy.
3. **Chống đếm trùng nằm ở ràng buộc `unique (ngan_hang, ma_gd)`** trong migration 0006,
   không nằm ở code. Nộp lại đúng file cũ thì `insert` vướng ràng buộc, bắt lỗi đó và
   xếp giao dịch vào nhóm "đã vào sổ" thay vì báo lỗi cho người dùng.

Deploy: `npx supabase functions deploy eda-doi-soat` (bỏ `--no-verify-jwt`, hai hàm này
**phải** yêu cầu đăng nhập, khác với `eda-register` là hàm công khai).

### B7.2 Gửi email

Tạo `eda-email` với ba mẫu và một bảng `eda_email_log` (gửi cho ai, mẫu nào, lúc nào, kết
quả) để không gửi trùng và để tra khi khách nói "em không nhận được".

| Mẫu | Khi nào |
|---|---|
| `dang-ky-nhan` | Ngay sau khi form đăng ký lưu thành công |
| `da-nhan-tien` | Sau khi kế toán bấm Xác nhận đã thu |
| `nhac-han` | Cron chạy hằng ngày, tìm đợt sắp tới hạn |

SMTP: dùng Brevo (miễn phí 300 thư/ngày). Khoá đặt ở Settings → Edge Functions → Secrets,
**không** đặt trong repo.

> **Địa chỉ email trong bảng là dữ liệu cá nhân của trẻ vị thành niên.** Đừng đưa danh
> sách này vào công cụ marketing nào, và đừng gửi thư hàng loạt ngoài ba mẫu trên.

### B7.3 Nội dung trang: chuyển từ trình duyệt sang máy chủ

**Hiện tại bản sửa chữ chỉ nằm trong trình duyệt của chính người sửa** (`localStorage`).
Người sửa bấm Xuất bản rồi mở lại trang thì thấy chữ mới, nhưng **khách vào vẫn thấy chữ
cũ**, và mở trên máy khác cũng thấy chữ cũ. Đủ để xem thử cách làm, chưa dùng thật được.

Bảng `eda_noi_dung` (migration 0008) đã có sẵn và đã kiểm phân quyền. Còn thiếu hai đầu:

1. **Trang quản trị ghi vào bảng** thay vì `localStorage`: đổi ba chỗ đọc/ghi
   `KHOA_LUU_NOI_DUNG` trong `admin.html` thành gọi PostgREST.
2. **Trang tuyển sinh đọc được bản đã xuất bản.** Đừng cho trang gọi thẳng Supabase: trang
   này là trang công khai, thêm một lần gọi mạng vào đường tải là chậm và là một thứ nữa
   có thể hỏng. Thay vào đó, một edge function `eda-xuat-ban-noi-dung` ghi ra file tĩnh
   `noi-dung.json`, trang tải file đó. Giữ nguyên nguyên tắc hiện có: **giá trị mặc định
   nằm trong markup**, file JSON chỉ chồng lên, để trang vẫn hiện đủ chữ khi file hỏng
   hoặc chưa có.

### B7.4 Học phí và ngân hàng thật

Hiện để `xx.xxx.xxx` và số đợt bịa. Có số thật thì điền vào `eda_payment_plan` và
`eda_plan_installment`. Ràng buộc ở migration 0005 canh cả hai phía: tổng các đợt phải
bằng tổng phương án, sai là không ghi được.

### Nhật ký giữ vĩnh viễn

**Có ý.** Không có cron xoá, không có hạn lưu. Nhật ký chỉ mất khi ai đó chủ động xoá bằng
tay trong SQL Editor của Supabase, và việc đó cần quyền cao hơn mọi vai của ứng dụng:
`revoke insert, update, delete, truncate` đã chặn cả ba vai lẫn `service_role` đi qua
PostgREST. Không thao tác nào từ trình duyệt xoá được một dòng nào.

Đổi lại, số điện thoại được **che ngay lúc ghi** nên bảng này không phải là bản sao dữ liệu
cá nhân, và giữ mãi cũng không tích tụ thứ đáng lo.

## B8. Những chỗ dễ vấp

| Chỗ | Chuyện gì xảy ra |
|---|---|
| Sửa `admin.html` import bằng `./` | Cả trang chết trắng ở mọi đường dẫn con |
| Thêm tab mà quên `_redirects` | F5 tại tab đó ra 404 hoặc ra trang tuyển sinh |
| Dùng `<input>` cho chữ nhiều dòng | Trình duyệt nuốt ký tự xuống dòng, tự "xuất bản" thay đổi không ai yêu cầu |
| Lọc `<style>` bằng regex viết hoa | Thẻ `<style>` trong `<svg>` có tên viết **thường**, lọt qua |
| Bật RLS mà quên policy SELECT | Không ai đọc được, kể cả quản trị, mà không báo lỗi gì |
| Thêm policy permissive cho một vai | Postgres **OR** các policy permissive. Mở cho một đường là mở cho cả bảng. |
| Tạo view mà quên cổng chặn | View bỏ qua RLS của bảng dưới. Người lạ đọc được qua view thứ mà bảng gốc đã cấm. |
| Hàm `security definer` không `revoke` | PostgREST bày nó thành endpoint `/rpc/…` gọi được bằng anon key |
| Dùng biểu thức `CASE` trong plpgsql cho hai bảng | Cả hai nhánh đều được phân giải, `new.cot_khong_co` sẽ nổ |
| Quên BOM khi xuất CSV | Excel mở ra tiếng Việt thành ký tự lạ |
| Dùng `toISOString()` đặt tên file | Ra ngày UTC, lệch với giờ ghi bên trong file |

### Bẫy màu ở dark mode

Trang có bảng màu riêng cho dark mode. Sửa màu thì phải kiểm **cả hai chế độ**: nhiều ô
nền sáng chữ tối ở light mode trở thành nền tối chữ tối ở dark mode. `scripts/audit_white_text.py`
dò các chỗ chữ trắng trên nền sáng.

---

## Giấy phép và dữ liệu cá nhân

Mã nguồn: xem [`LICENSE`](LICENSE).

Bảng `eda_registration` chứa **dữ liệu cá nhân của trẻ vị thành niên** (họ tên, số điện
thoại, số điện thoại phụ huynh). Không sao chép ra ngoài Supabase, không đưa vào repo,
không gửi qua chat. Sao kê ngân hàng cũng vậy: đọc trong trình duyệt, không lưu lại file.

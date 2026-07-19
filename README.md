# eDA 2026 · Trang tuyển sinh End2End Data Analytics

### 🔗 Xem trang chạy thật: **https://eda.luonvuituoi.work**

> Đây là **bản xem thử**. Form đăng ký chưa lưu được vì Supabase chưa dựng (xem mục 4),
> điền vào sẽ báo lỗi chứ không báo thành công giả.

Trang tuyển sinh khoá **End2End Data Analytics 2026** của AI VIETNAM, kèm backend nhận
đăng ký và trang quản trị xem danh sách.

Khai giảng 06.09.2026, kết thúc 05.2027. 8 module, 9 domain, 100 buổi live online.

```
┌─ Trình duyệt ────────────┐      ┌─ Supabase ──────────────────────────┐
│ TuyenSinh-eDA2026.dc.html│─POST→│ edge function  eda-register         │
│  (trang tuyển sinh)      │      │   ↓ service-role key                │
│                          │      │ bảng  public.eda_registration (RLS) │
│ admin.html               │←GET──│   ↑ PostgREST + Realtime            │
│  (xem danh sách)         │      │     chỉ role EDA_ADMIN đọc được     │
└──────────────────────────┘      └─────────────────────────────────────┘
```

---

## 1. Chạy thử tại máy

Trang là file tĩnh, nhưng **không mở trực tiếp bằng `file://` được**: mỗi tab là một
đường dẫn thật (`/pathway`, `/docs`…) nên cần một web server biết trả về trang chính cho
mọi đường dẫn lạ.

### Cách nhanh nhất (Docker)

```bash
cd docker
docker compose up -d
```

Mở http://localhost:8791

Dừng: `docker compose down`. Cấu hình nằm ở `docker/nginx-eda.conf`, thư mục gốc repo
được gắn vào read-only nên sửa file là F5 thấy ngay.

### Không có Docker

Cần một server có URL rewrite. Ví dụ với Python thì **không dùng được**
`http.server` (nó không rewrite). Dùng `npx serve` với cấu hình rewrite, hoặc cài nginx
và chép `docker/nginx-eda.conf`.

### Kiểm tra sau khi chạy

| Việc | Kỳ vọng |
|---|---|
| Mở `/` | Tab Tổng quan |
| Mở thẳng `/pathway` rồi F5 | Tab Lộ trình học, **không 404** |
| Bấm qua lại các tab | URL đổi theo, nút Back trình duyệt hoạt động |
| `node scripts/test-bao-mat.mjs` | 14 kiểm tra đều đạt |

---

## 2. Cấu trúc thư mục

| Đường dẫn | Là gì |
|---|---|
| `TuyenSinh-eDA2026.dc.html` | **Toàn bộ trang tuyển sinh**, một file duy nhất (~250KB) |
| `admin.html` | Trang quản trị, xem và tải CSV danh sách đăng ký |
| `support.js` | Runtime DesignCombo cho `.dc.html` (không sửa) |
| `image-slot.js` | Web component khung ảnh (không sửa) |
| `globe.html` | Quả địa cầu, nhúng bằng iframe vào trang chính |
| `map-vietnam.html` | Bản đồ Việt Nam (hiện chưa dùng) |
| `assets/` | Logo, hoạ tiết trống đồng, ảnh thumbnail video |
| `ava/` | Ảnh 4 giảng viên. `crop-*.jpg` là bản đang dùng, còn lại là ảnh gốc |
| `data/` | File nguồn: `eDA_v9.xlsx` (giáo trình), sơ đồ drawio, ghi chú |
| `docker/` | nginx + compose để chạy thử |
| `docs/` | Tài liệu dự án, quan trọng nhất là `deployment-guide.md` |
| `scripts/` | Script Python sinh nội dung từ Excel, và test bảo mật |
| `supabase/` | Migration SQL + edge function nhận đăng ký |

### Về file `.dc.html`

Đây là định dạng **DesignCombo**: HTML thường cộng thêm runtime phản ứng trong
`support.js`. Cú pháp riêng cần biết:

| Cú pháp | Nghĩa |
|---|---|
| `{{ bien }}` | Chèn giá trị từ state |
| `<sc-if value="{{ dk }}">` | Hiện khối khi điều kiện đúng |
| `<sc-for>` | Lặp danh sách |
| `<helmet>` | Nội dung đẩy vào `<head>` |
| `<x-import>` | Nhúng web component |
| `class Component extends DCLogic` | Khối logic ở cuối file, có `state` và `renderVals()` |

Trang có 6 tab, mỗi tab một đường dẫn. Bảng ánh xạ nằm ở hằng số `TAB_SLUGS`:

```js
const TAB_SLUGS = ['', 'pathway', 'early', 'docs', 'mentors', 'register'];
```

Đổi slug thì phải sửa cả `docs/deployment-guide.md` và comment trong
`docker/nginx-eda.conf`.

---

## 3. Sinh lại nội dung từ file nguồn

Một số phần trong trang **không gõ tay** mà sinh ra từ `data/eDA_v9.xlsx`. Sửa Excel rồi
chạy lại script thì trang tự cập nhật:

```bash
python scripts/build-domain-matrix.py     # bảng 10 ngành × 10 mảng phân tích
python scripts/build-overview-diagram.py  # sơ đồ tổng quan
python scripts/build-syllabus-html.py     # lịch chi tiết từng module
```

Script tự tìm khối đã chèn lần trước bằng comment mốc và thay đúng khối đó, nên chạy lại
nhiều lần được, không sinh trùng.

> `scripts/` còn khoảng 40 file `fix_*.py`, `update_*.py` là script dùng một lần trong
> quá trình làm. Không cần chạy lại. Giữ để tra cứu lịch sử chỉnh sửa.

---

## 4. Dựng backend lưu đăng ký

**Chưa làm bước này thì form đăng ký không lưu được gì.** Toàn bộ chi tiết nằm ở
[`docs/deployment-guide.md`](docs/deployment-guide.md). Tóm tắt 6 bước:

### 4.1 Tạo project Supabase

Dùng **project riêng cho eDA**, đừng ghép chung với dự án khác. Lý do: bảng đăng ký chứa
số điện thoại phụ huynh của trẻ vị thành niên, tách riêng thì phân quyền và xoá dữ liệu
sau này đều gọn.

Ghi lại `Project URL` và `anon key` ở Settings → API.

### 4.2 Chạy migration

SQL Editor, chạy lần lượt 4 file trong `supabase/migrations/` theo đúng thứ tự số.

### 4.3 Deploy edge function

```bash
npx supabase login
npx supabase link --project-ref <ref-cua-ban>
npx supabase functions deploy eda-register --no-verify-jwt
```

Rồi đặt biến môi trường ở Settings → Edge Functions → Secrets. Bảng đầy đủ trong
deployment guide; **bắt buộc** là `EDA_ALLOWED_ORIGINS`.

### 4.4 Điền các chỗ `REPLACE-ME`

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

### 4.5 Tạo tài khoản quản trị

Authentication → Users → Add user. Đặt mật khẩu ngẫu nhiên **ngay trong màn hình đó**,
lưu vào trình quản lý mật khẩu. Không ghi vào repo, không gửi qua chat.

Rồi cấp quyền trong SQL Editor:

```sql
update auth.users
   set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb)
                           || '{"role":"EDA_ADMIN"}'::jsonb
 where email = 'admin@aivietnam.edu.vn';
```

Tài khoản phải **đăng xuất rồi đăng nhập lại** thì token mới mang quyền. Thiếu bước này
thì đăng nhập vẫn được nhưng bảng trống trơn.

> Đừng dùng số hotline làm mật khẩu. Số `0911 118 758` đang in công khai ở chân trang.

### 4.6 Bật rewrite trên host

| Host | Cấu hình |
|---|---|
| nginx | `try_files $uri /TuyenSinh-eDA2026.dc.html;` |
| Vercel | `vercel.json`: `{"rewrites":[{"source":"/(.*)","destination":"/TuyenSinh-eDA2026.dc.html"}]}` |
| Cloudflare Pages | file `_redirects`, xem sẵn trong repo |

Thiếu bước này thì bấm tab vẫn chạy, nhưng F5 hoặc mở link chia sẻ sẽ 404.

### Riêng Cloudflare Pages (bản đang chạy)

```bash
node scripts/dung-thu-muc-xuat-ban.mjs
npx wrangler pages deploy .xuat-ban --project-name eda --branch master
```

**Phải deploy từ `.xuat-ban`, đừng deploy từ thư mục gốc.** `wrangler pages deploy`
không đọc `.gitignore` (cũng không đọc `.assetsignore`), nên deploy từ gốc là
`data/eDA_v9.xlsx`, toàn bộ migration SQL và tài liệu PDF đều thành URL công khai.
Script trên chép ra đúng 17 file trang thật sự cần, khoảng 1.1MB.

Hai điểm khác nginx, đã ghi trong `_redirects`:

- Pages **tự cắt đuôi `.html`**, nên đích phải là `/TuyenSinh-eDA2026.dc` không kèm
  `.html`, nếu không Pages trả 308 và mọi tab bị dồn về một địa chỉ.
- **Đừng dùng luật `/*`.** Trên Pages nó nuốt cả file có thật, `support.js` và ảnh đều
  bị trả về HTML nên trang không nạp được runtime. Phải liệt kê từng đường dẫn tab.

Hai chỗ dễ vấp: **đừng thêm `$uri/` vào `try_files`** (repo có thư mục `docs/` trùng tên
slug `/docs`), và trang đang đặt `<base href="/">` nên **phải deploy ở gốc tên miền**.

---

## 5. Bảo mật

Bảng `eda_registration` chứa họ tên, số điện thoại, email của học viên, và **tên + số
điện thoại người giám hộ của trẻ vị thành niên**. Các lớp bảo vệ hiện có:

| Lớp | Cách làm |
|---|---|
| Chặn đọc trộm | RLS bật, không policy nào cho `anon`. Chỉ tài khoản có `app_metadata.role = 'EDA_ADMIN'` đọc được, và Realtime cũng đi qua RLS |
| Chặn ghi trộm | Không cấp `insert` cho ai. Ghi chỉ qua edge function bằng service-role key |
| Chặn nhúng chéo | `EDA_ALLOWED_ORIGINS` giới hạn tên miền gọi được endpoint |
| Chặn bot | Honeypot + giới hạn 10 đơn/IP/giờ (băm IP, không lưu IP thô) |
| Chặn chiếm trang admin | CSP `default-src 'none'`, script pin phiên bản + SRI, `frame-ancestors 'none'` |
| Chặn CSV injection | Ô bắt đầu bằng `= + - @` được thêm dấu nháy, tránh Excel chạy công thức do người đăng ký cài vào |
| Giảm thời gian phơi nhiễm | Cron xoá đơn cũ hơn 24 tháng |

Chạy kiểm tra:

```bash
node scripts/test-bao-mat.mjs
```

### Việc còn phải làm

- **Không có CAPTCHA**, đây là lựa chọn có chủ đích. Chống bot chỉ gồm honeypot và giới
  hạn tần suất theo IP, nên một bot chịu khó vẫn gửi được đơn rác. Đổi lại người đăng ký
  thật không vướng màn kiểm tra nào. Đơn rác nhiều thì hạ `EDA_MAX_PER_HOUR` trước.
- **Không có nhật ký truy cập.** Ai đăng nhập admin, ai tải CSV đều không ghi lại.
- **Chưa có backup.** Supabase Free không tự sao lưu; nên xuất CSV định kỳ.

---

## 6. Những chỗ dễ vấp

| Hiện tượng | Nguyên nhân |
|---|---|
| Sửa file mà trình duyệt không đổi | Cache. Bấm **Ctrl+Shift+R**. iframe (`globe.html`) và ảnh cứng đầu nhất |
| F5 ở `/pathway` ra 404 | Host chưa bật rewrite, xem mục 4.6 |
| `/docs` ra danh sách thư mục | `try_files` có `$uri/`, bỏ đi |
| Đăng nhập admin không phản hồi | `REPLACE-ME` trong CSP `connect-src` chưa điền |
| Đăng nhập được nhưng bảng trống | Tài khoản chưa gán `EDA_ADMIN`, hoặc chưa đăng xuất/đăng nhập lại |
| Gửi đăng ký báo lỗi 403 | `EDA_ALLOWED_ORIGINS` chưa có tên miền hiện tại |
| Gửi đăng ký báo lỗi 429 | Vượt `EDA_MAX_PER_HOUR` (mặc định 10 đơn/IP/giờ) |
| Chữ tàng hình ở dark mode | Xem mục dưới |

### Bẫy màu ở dark mode

Đã sửa hết, nhưng nếu thêm khối mới thì dễ dính lại. Hai kiểu:

1. `background: var(--ink)` trên **cùng element** có khai `--ink: ...`. Custom property
   khai trên element áp luôn cho `background` của chính nó, nên nền ra sai màu. Dải tối
   cố định thì dùng màu cứng.
2. Khai `--ink` nhưng **quên đặt `color`**. `--ink` chỉ ăn vào thuộc tính nào dùng
   `var(--ink)` trên element đó (border, box-shadow). `color` thì kế thừa giá trị đã
   tính từ cha. Nền sáng cứng phải kèm `color: var(--ink,#211d17)`.

---

## 7. Giấy phép và dữ liệu cá nhân

Mã nguồn theo `LICENSE`. Nhưng **nội dung không phải mã nguồn thì không**:

- `ava/*.jpg` là ảnh chân dung 4 giảng viên có tên thật. Dùng lại phải xin phép.
- `data/eDA_v9.xlsx`, sơ đồ, nội dung giáo trình là tài sản của AI VIETNAM.
- Logo và hoạ tiết trong `assets/` cũng vậy.

Tài liệu đọc của khoá học **không nằm trong repo**, phát cho học viên qua link Drive.

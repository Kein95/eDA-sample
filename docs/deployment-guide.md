# Triển khai eDA 2026

Trang tuyển sinh là file tĩnh. Phần cần dựng là backend nhận đăng ký trên Supabase.

## 1. Tạo Supabase project

Khuyến nghị **project riêng cho eDA**, không dùng chung với IAIO. Lý do: bảng đăng ký
chứa họ tên và số điện thoại phụ huynh của trẻ vị thành niên. Tách riêng thì phân
quyền, sao lưu và xoá dữ liệu sau này đều gọn.

Ghi lại `Project URL` và `anon key` (Settings → API).

## 2. Chạy migration

Chạy theo thứ tự, trong SQL Editor:

| File | Nội dung |
|---|---|
| `supabase/migrations/0001_eda_registration.sql` | bảng `eda_registration`, bật RLS, không policy |
| `supabase/migrations/0002_eda_registration_admin_read.sql` | policy cho `EDA_ADMIN` đọc |
| `supabase/migrations/0003_eda_realtime_and_keepalive.sql` | realtime + pg_cron chống ngủ |
| `supabase/migrations/0004_eda_rate_limit_and_retention.sql` | cột `ip_hash` + cron xoá dữ liệu quá 24 tháng |

## 3. Deploy edge function

```bash
supabase functions deploy eda-register --no-verify-jwt
```

Biến môi trường (Settings → Edge Functions → Secrets):

| Tên | Bắt buộc | Ghi chú |
|---|---|---|
| `EDA_ALLOWED_ORIGINS` | **trước khi chạy thật** | danh sách tên miền ngăn bởi dấu phẩy, ví dụ `https://aivietnam.edu.vn`. Để trống = nhận từ mọi tên miền (chỉ hợp lúc chạy thử) |
| `EDA_IP_SALT` | nên đặt | chuỗi ngẫu nhiên để băm IP phục vụ giới hạn tần suất. Không đặt thì dùng tạm service-role key |
| `EDA_MAX_PER_HOUR` | không | số đơn tối đa mỗi IP mỗi giờ, mặc định `10` |
| `RESEND_API_KEY` | không | có thì gửi email xác nhận cho người đăng ký |
| `EDA_EMAIL_FROM` | không | mặc định `no-reply@aivietnam.edu.vn` |

> **Không dùng CAPTCHA.** Chống bot dựa vào honeypot (trường ẩn trong form) và giới hạn
> tần suất theo IP. Đánh đổi: bot chịu khó vẫn gửi được đơn rác, bù lại người đăng ký
> thật không phải qua màn kiểm tra nào, và không có biến môi trường nào xoá nhầm là
> tắt bảo vệ âm thầm. Nếu về sau lượng đơn rác thành vấn đề thì hạ `EDA_MAX_PER_HOUR`
> trước đã, rồi mới tính tới CAPTCHA.

`SUPABASE_URL` và `SUPABASE_SERVICE_ROLE_KEY` Supabase tự cấp, không cần khai.

## 4. Điền 3 chỗ `REPLACE-ME`

| File | Hằng số |
|---|---|
| `TuyenSinh-eDA2026.dc.html` | `EDA_REGISTER_ENDPOINT` |
| `admin.html` | `SUPABASE_URL`, `SUPABASE_ANON_KEY` |

`admin.html` còn có **CSP trong thẻ `<meta>` ở đầu file**, trong đó `connect-src` cũng ghi
`REPLACE-ME`. Sửa cả hai URL ở dòng đó (`https://` và `wss://`), nếu không thì đăng nhập
và Realtime đều bị trình duyệt chặn.

`anon key` là khoá công khai theo thiết kế, để lộ không sao. Thứ chặn truy cập là RLS.

## 5. Tạo tài khoản quản trị

Authentication → Users → Add user, email `admin@aivietnam.edu.vn`.

Đặt mật khẩu **ngay trong màn hình đó**. Không ghi mật khẩu vào repo, không gửi qua chat.

Sau đó cấp quyền (SQL Editor):

```sql
update auth.users
   set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb)
                           || '{"role":"EDA_ADMIN"}'::jsonb
 where email = 'admin@aivietnam.edu.vn';
```

Tài khoản phải **đăng xuất rồi đăng nhập lại** thì token mới mang quyền.

> **Không dùng số hotline làm mật khẩu.** Số `0911 118 758` đang in công khai ở nút Zalo
> và chân trang, ai đọc trang cũng biết. Bảng này chứa số điện thoại phụ huynh của
> học sinh chưa đủ tuổi, nên mật khẩu phải là chuỗi ngẫu nhiên, lưu trong trình quản lý
> mật khẩu.

## 6. Bật rewrite cho đường dẫn tab

Mỗi tab là một đường dẫn thật: `/` (Tổng quan), `/pathway`, `/early`, `/docs`,
`/mentors`, `/register`. Trang chỉ có một file `TuyenSinh-eDA2026.dc.html`, nên host
phải trả file đó cho mọi đường dẫn không khớp file có thật. **Thiếu bước này thì
trang vẫn chạy khi bấm tab, nhưng F5 hoặc mở link chia sẻ sẽ 404.**

| Host | Cấu hình |
|---|---|
| nginx (đang dùng ở `docker/nginx-eda.conf`) | `try_files $uri /TuyenSinh-eDA2026.dc.html;` |
| Vercel | `vercel.json`: `{"rewrites":[{"source":"/(.*)","destination":"/TuyenSinh-eDA2026.dc.html"}]}` |
| Netlify | `_redirects`: `/*  /TuyenSinh-eDA2026.dc.html  200` |
| Cloudflare Pages | `_redirects` giống Netlify |

Hai điểm dễ vấp:

- **Đừng thêm `$uri/` vào `try_files`.** Repo có thư mục `docs/` trùng tên với đường
  dẫn tab `/docs`; có `$uri/` thì nginx sẽ 301 sang `/docs/` và liệt kê thư mục thay vì
  mở tab Tài liệu.
- Trang đang đặt `<base href="/">`, tức là **phải deploy ở gốc tên miền**. Nếu đặt dưới
  đường dẫn con (ví dụ `aivietnam.edu.vn/eda-2026`) thì phải sửa `base` và `TAB_SLUGS`
  cho khớp, nếu không ảnh và đường dẫn tab đều trỏ sai.

## 7. Kiểm tra sau khi deploy

1. Gửi thử một đăng ký trên trang, xem có dòng mới trong `eda_registration` không.
2. Ngắt mạng rồi gửi lại: trang phải **báo lỗi**, không được hiện màn "đã nhận".
3. Mở `admin.html`, đăng nhập, thấy đúng dòng vừa tạo.
4. Mở admin ở một cửa sổ, gửi đăng ký ở cửa sổ khác: dòng mới phải tự nhảy vào
   (chấm "đang nhận trực tiếp" màu xanh).
5. Sau một ngày, kiểm tra `select * from public.eda_keepalive` xem cron có chạy không.
6. Mở thẳng `/pathway` rồi F5: phải ra tab Lộ trình, không được 404. Làm tương tự với
   `/early`, `/docs`, `/mentors`, `/register`.

## Không cần dùng tới

Storage, pgvector, Queues, Branching: dự án không có nhu cầu. Thêm vào chỉ tốn công
bảo trì.

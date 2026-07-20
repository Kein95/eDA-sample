# Đợt 3 — Sửa nội dung trang không đụng code

Không phụ thuộc đợt 1 và 2, làm song song được.

## Vấn đề

Toàn bộ chữ, giá, lịch của trang tuyển sinh nằm cứng trong markup của
`TuyenSinh-eDA2026.dc.html`. Đổi một con số là phải sửa code, build lại, deploy lại.

## Phạm vi cố ý hẹp: chỉ chữ và số

CMS làm được **sửa nội dung có sẵn**, không làm được **thêm/bớt/đổi thứ tự khối**.

Lý do: trang này không phải bố cục lưới thông thường mà là một thiết kế đã căn tay kỹ —
chip 8 module, dải ngang, quả địa cầu, timeline chevron. Cho phép thêm khối tuỳ ý đồng
nghĩa với việc mọi thay đổi nội dung đều có thể phá bố cục, và sẽ cần một trình dựng
trang thật sự. Đó là một sản phẩm khác, không phải một đợt trong kế hoạch này.

Nếu sau này thật sự cần thêm/bớt khối thì mở riêng, đừng nong đợt này ra.

## Cách làm

### Bảng

```sql
create table public.eda_noi_dung (
  khoa        text primary key,           -- 'hero.tieu_de', 'hoc_phi.pa1.tong'
  gia_tri     text not null,
  kieu        text not null default 'text' check (kieu in ('text','so','ngay','html_han_che')),
  mo_ta       text not null,              -- hiện cho người sửa biết đây là chỗ nào
  sua_boi     uuid references auth.users(id),
  sua_luc     timestamptz not null default now()
);
```

`kieu = 'html_han_che'` chỉ cho `<b> <i> <br> <a>`, lọc ở lúc ghi chứ không phải lúc
đọc. Người sửa nội dung không được phép chèn `<script>` vào trang công khai — đây là
XSS do người trong nhà gây ra, vẫn là XSS.

### Trang đọc nội dung thế nào

**Không** để trang gọi Supabase lúc tải. Trang tuyển sinh phải hiện đủ ngay cả khi
Supabase ngủ hoặc chết — free tier có ngủ, và một trang tuyển sinh trắng chữ vì DB
không phản hồi là hỏng nặng hơn nội dung cũ vài phút.

Cách làm:

1. Nội dung mặc định **vẫn nằm trong markup** như hiện nay
2. Trang tải xong thì `fetch('/noi-dung.json')`, thấy khoá nào thì chồng lên khoá đó
3. `fetch` hỏng hoặc chậm → không sao, nội dung mặc định đã hiển thị rồi

`noi-dung.json` là file tĩnh trên Cloudflare Pages, không phải API. Bấm "Xuất bản" ở
trang quản trị thì sinh lại file này và deploy. Đọc nội dung không tốn một truy vấn DB nào.

Đánh dấu chỗ chồng nội dung bằng `data-noi-dung="hero.tieu_de"` trên chính thẻ đang có
nội dung mặc định, để hai bên không lệch nhau.

### Giao diện sửa

Tab "Nội dung" trong `admin.html`: bảng khoá / mô tả / ô nhập, nút Lưu nháp và nút
Xuất bản. Nhóm theo tiền tố khoá (`hero.*`, `hoc_phi.*`) cho dễ tìm.

Tách **lưu** và **xuất bản**: sửa nửa chừng mà đã lên trang công khai là chuyện không
nên xảy ra.

## Việc phải làm

1. Migration `0007_eda_noi_dung.sql` + RLS (đọc: mọi vai; ghi: vai biên tập trở lên)
2. Rà `TuyenSinh-eDA2026.dc.html`, gắn `data-noi-dung` vào những chỗ thật sự hay đổi —
   tiêu đề, học phí, lịch, hạn Early Bird. **Không** gắn tràn lan.
3. Đoạn script chồng nội dung (~20 dòng, đặt cuối trang)
4. Edge function `eda-xuat-ban-noi-dung`: đọc bảng, sinh JSON, đẩy lên Pages
5. Tab "Nội dung" trong admin

## Kiểm chứng

- Chặn `/noi-dung.json` (mô phỏng mạng hỏng) → trang vẫn hiện đủ nội dung mặc định
- Sửa học phí ở admin → bấm Xuất bản → tải lại trang thấy số mới
- Sửa nhưng chưa Xuất bản → trang công khai vẫn số cũ
- Nhập `<script>alert(1)</script>` vào ô nội dung → bị lọc lúc ghi, trang không chạy script
- Khoá có trong JSON nhưng không còn trong markup → bỏ qua im lặng, không lỗi

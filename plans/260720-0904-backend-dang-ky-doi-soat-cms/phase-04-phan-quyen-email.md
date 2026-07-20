# Đợt 4 — Phân quyền theo vai + email

Phụ thuộc đợt 1 và 2.

## Phân quyền

Hiện chỉ có một vai `EDA_ADMIN` trong `app_metadata` (migration 0002). Một vai thì hoặc
mở hết hoặc không cho vào — không diễn tả được "người này sửa nội dung được nhưng không
đụng tiền".

Đề xuất **4 vai**, không phải 6 như LVT-AR:

| Vai | Xem đăng ký | SĐT phụ huynh | Đối soát tiền | Sửa nội dung | Cấp quyền |
|---|---|---|---|---|---|
| `EDA_VIEWER` | ✓ | ✗ | ✗ | ✗ | ✗ |
| `EDA_EDITOR` | ✓ | ✗ | ✗ | ✓ | ✗ |
| `EDA_FINANCE` | ✓ | ✓ | ✓ | ✗ | ✗ |
| `EDA_ADMIN` | ✓ | ✓ | ✓ | ✓ | ✓ |

Bốn vai vì đó là số lượng ranh giới thật sự tồn tại ở đây: xem, sửa chữ, đụng tiền, cấp
quyền. Thêm vai chỉ để đủ bộ là tạo ra thứ phải bảo trì mà không ai dùng.

**Cột nhạy cảm tách riêng.** `guardian_name` và `guardian_phone` là dữ liệu liên lạc của
người giám hộ trẻ vị thành niên. RLS của Postgres chặn theo dòng, không chặn theo cột,
nên phải làm bằng view:

```sql
create view public.eda_registration_an_toan as
select id, code, name, phone, email, province, job, field, interest,
       facebook, zalo, channel, note, plan_id, trang_thai, created_at
  from public.eda_registration;   -- KHÔNG có guardian_*
```

`EDA_VIEWER` và `EDA_EDITOR` chỉ được select trên view này. `EDA_FINANCE` và
`EDA_ADMIN` select được trên bảng gốc.

Giữ nguyên cách đọc vai từ `app_metadata` chứ không phải `user_metadata` — lý do đã ghi
rõ trong 0002: `user_metadata` do chính người dùng sửa được.

## Email

Dùng lại hạ tầng sẵn có của `luonvuituoi.work`: Brevo SMTP. Không thêm dịch vụ mới.

Ba loại thư:

| Loại | Khi nào | Nội dung |
|---|---|---|
| `dang-ky-nhan` | ngay sau khi đăng ký | mã giữ chỗ, hướng dẫn CK, ảnh QR, **nội dung CK in đậm** |
| `da-nhan-tien` | khi xác nhận giao dịch | đợt nào, bao nhiêu, còn nợ bao nhiêu |
| `nhac-han` | thủ công, có nút gửi lại | đợt sắp tới hạn hoặc quá hạn |

Hai điều học từ VNCLO (`mail.service.ts`):

1. **Chống gửi trùng**: chỉ gửi `da-nhan-tien` khi trạng thái cũ chưa phải đã xác nhận.
   Xác nhận lại lần hai không được gửi thư lần hai.
2. **Chưa cấu hình SMTP thì im lặng bỏ qua**, không làm hỏng luồng đăng ký. Người đăng ký
   mất một cái email còn hơn mất cả đơn đăng ký.

Thêm một điều VNCLO không có: **bảng `eda_email_log`** (gửi cho ai, loại gì, lúc nào,
kết quả). Không có log thì không trả lời được "tôi không nhận được email nào cả".

Chưa làm cron nhắc hạn tự động ở đợt này — nút gửi thủ công trước, xem thực tế cần gì.

## Việc phải làm

1. Migration `0008_eda_phan_quyen.sql`: view an toàn, policy cho 4 vai, thay policy cũ ở 0002
2. Migration `0009_eda_email_log.sql`
3. Edge function `eda-email` với 3 loại thư
4. Nối `eda-register` gọi `dang-ky-nhan`, `eda-xac-nhan-gd` gọi `da-nhan-tien`
5. Trang admin: ẩn tab theo vai, đọc từ JWT

## Kiểm chứng

- Tài khoản `EDA_VIEWER` gọi thẳng REST API lấy `guardian_phone` → phải bị từ chối. Test
  bằng HTTP thật, không phải bằng việc ẩn nút trên giao diện.
- Tài khoản `EDA_EDITOR` gọi API xác nhận giao dịch → bị từ chối
- Xác nhận cùng một giao dịch hai lần → chỉ một email
- Tắt cấu hình SMTP → đăng ký vẫn thành công, chỉ không có thư
- Mọi thư gửi đi đều có dòng trong `eda_email_log`

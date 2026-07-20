# Đợt 4 — Phân quyền theo vai + email

Phụ thuộc đợt 1 và 2.

## Phân quyền

Hiện chỉ có một vai `EDA_ADMIN` trong `app_metadata` (migration 0002). Một vai thì hoặc
mở hết hoặc không cho vào — không diễn tả được "người này sửa nội dung được nhưng không
đụng tiền".

**3 vai**, đặt theo chức danh có thật trong đội:

| Vai | Xem học viên | SĐT phụ huynh | Số tiền, giao dịch | Đối soát | Sửa nội dung | Cấp quyền |
|---|---|---|---|---|---|---|
| `EDA_TA` (trợ giảng) | ✓ | ✗ | chỉ "đã đủ / còn nợ" | ✗ | ✗ | ✗ |
| `EDA_ACCOUNTANT` (kế toán) | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `EDA_ADMIN` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Đây là ba chức danh thật, không phải ba mức quyền bịa ra. Bản trước tôi đề xuất thêm
`VIEWER` và `EDITOR`: ở quy mô này không ai làm đúng hai việc đó cả, chúng là vai trống.
Sửa nội dung gộp vào admin.

**Trợ giảng cần biết ai còn nợ** để biết ai được vào lớp, nhưng không cần biết nợ bao
nhiêu hay ai chuyển khoản lúc nào. Nên view của TA có thêm đúng một cột `da_dong_du`
(boolean), không có số tiền.

**Trợ giảng không thấy liên lạc người giám hộ.** Trợ giảng đuổi bài, điểm danh thì liên
hệ thẳng học viên; còn chuyện tiền nong với phụ huynh là việc của kế toán. Nếu thực tế
vận hành cần khác thì mở, nhưng mặc định nên đóng — đây là số điện thoại phụ huynh của
trẻ vị thành niên.

Nếu chưa có ai làm trợ giảng thì đừng tạo tài khoản; bản thân vai chỉ tốn vài dòng
policy, nhưng một tài khoản không ai dùng là một tài khoản không ai để ý khi bị chiếm.

**Cột nhạy cảm tách riêng.** `guardian_name` và `guardian_phone` là dữ liệu liên lạc của
người giám hộ trẻ vị thành niên. RLS của Postgres chặn theo dòng, không chặn theo cột,
nên phải làm bằng view:

```sql
create view public.eda_registration_tro_giang as
select r.id, r.code, r.name, r.phone, r.email, r.province, r.job, r.field,
       r.interest, r.facebook, r.zalo, r.channel, r.note, r.trang_thai, r.created_at,
       -- Du de biet ai duoc vao lop, khong lo ra so tien.
       (n.da_dong >= n.phai_dong) as da_dong_du
  from public.eda_registration r
  left join public.eda_cong_no n on n.registration_id = r.id;
  -- KHONG co guardian_name, guardian_phone, khong co so tien
```

`EDA_TA` chỉ select được trên view này. `EDA_ACCOUNTANT` và `EDA_ADMIN` select được
trên bảng gốc.

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

- Tài khoản `EDA_TA` gọi thẳng REST API lấy `guardian_phone` → phải bị từ chối. Test
  bằng HTTP thật, không phải bằng việc ẩn nút trên giao diện.
- Tài khoản `EDA_TA` gọi API xác nhận giao dịch → bị từ chối
- Tài khoản `EDA_ACCOUNTANT` gọi API sửa nội dung trang → bị từ chối
- Xác nhận cùng một giao dịch hai lần → chỉ một email
- Tắt cấu hình SMTP → đăng ký vẫn thành công, chỉ không có thư
- Mọi thư gửi đi đều có dòng trong `eda_email_log`

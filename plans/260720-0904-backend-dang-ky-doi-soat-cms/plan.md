# eDA 2026 — Backend đăng ký, đối soát chuyển khoản, CMS

Trạng thái: **chưa bắt đầu** · Tạo 20/07/2026

## Bối cảnh

Hiện eDA là một trang `.dc.html` tĩnh + `admin.html` chỉ đọc, chưa nối backend. Phần
Supabase đã viết dở và viết tốt: 4 migration (RLS, băm IP, cron dọn dữ liệu 24 tháng,
keepalive) + edge function `eda-register`. Kế hoạch này **làm tiếp trên nền đó**, không
thay stack.

Quyết định đã chốt với người dùng 20/07:

- Dựng mới cho eDA (không fork VNCLO, không gắn vào LVT-AR)
- Đợt 1 làm cả đăng ký + đối soát **và** CMS

Tham chiếu đã khảo sát: `D:\Projects\VNCLO\vnclo` có sẵn luồng đối soát sao kê đáng học
(upload .xls Vietcombank, regex bắt mã + SĐT, preview rồi người xác nhận, không bao giờ
tự ghi). IAIO không có phần thanh toán (thi miễn phí, cắt bỏ có chủ đích).

## Hai rủi ro quyết định thiết kế

**1. Đếm tiền hai lần.** VNCLO không có bảng giao dịch; upload lại cùng file sao kê là
khớp lại từ đầu. Nó thoát lỗi chỉ vì mỗi thí sinh trả đúng một lần 500k. eDA có nhiều
đợt nên bắt buộc phải có `eda_bank_txn` với **UNIQUE trên mã giao dịch ngân hàng** —
đây là thứ chặn đếm trùng, không phải logic ứng dụng.

**2. Một cờ true/false không diễn tả được "đã đóng đợt 2/4".** Phải materialize từng
đợt thành một dòng cho mỗi người đăng ký, vì thực tế có học bổng, giảm học phí, và
đóng thiếu.

## Phân đợt

| Đợt | Nội dung | Phụ thuộc | File |
|---|---|---|---|
| 1 | Schema học phí, đợt đóng, giao dịch ngân hàng | — | [phase-01](phase-01-schema-hoc-phi-giao-dich.md) |
| 2 | Đối soát sao kê: upload, khớp, xác nhận | 1 | [phase-02](phase-02-doi-soat-sao-ke.md) |
| 3 | CMS sửa nội dung trang không đụng code | — (song song 1) | [phase-03](phase-03-cms-noi-dung.md) |
| 4 | Phân quyền theo vai + email tự động | 1, 2 | [phase-04](phase-04-phan-quyen-email.md) |

Đợt 3 không phụ thuộc 1 và 2, có thể làm song song.

## Tiêu chí nghiệm thu toàn cục

- Upload **cùng một file sao kê hai lần** không làm thay đổi số dư của bất kỳ ai. Đây là
  test bắt buộc, không phải tuỳ chọn.
- Không thao tác nào tự động ghi tiền vào DB; mọi lần ghi đều do người bấm xác nhận và
  đều để lại dòng trong `eda_audit`.
- Người có vai xem danh sách không đọc được số điện thoại phụ huynh (dữ liệu trẻ vị
  thành niên) trừ khi được cấp riêng.
- Trang tuyển sinh vẫn hiển thị đầy đủ khi Supabase chết: nội dung CMS chỉ chồng lên
  nội dung mặc định đã nhúng sẵn, không thay thế.
- Migration chạy lại lần hai không sinh cron job trùng (đã theo đúng cách của 0003/0004).

## Câu chưa có lời giải

1. **eDA thu học phí bao nhiêu, mấy phương án, mấy đợt, mốc ngày nào?** Trang hiện không
   có học phí ở bất kỳ tab nào. Ví dụ AIO (3 phương án, 2–5 đợt) chỉ cho biết *kiểu*
   cấu trúc, không phải số thật của eDA. Schema ở đợt 1 thiết kế tổng quát nên không bị
   chặn, nhưng **không seed được dữ liệu thật** cho tới khi có câu trả lời.
2. **Ngân hàng nhận tiền là ngân hàng nào?** Parser sao kê phụ thuộc layout từng ngân
   hàng. VNCLO hardcode Vietcombank và sẽ hỏng nếu đổi.
3. Có cần hoá đơn/biên lai cho người đóng tiền không (ảnh hưởng schema và nghĩa vụ thuế)?
4. CMS cho sửa tới đâu: chỉ chữ và số, hay cả thêm/bớt khối nội dung? Đợt 3 hiện giả
   định **chỉ chữ và số** — xem lý do trong phase-03.

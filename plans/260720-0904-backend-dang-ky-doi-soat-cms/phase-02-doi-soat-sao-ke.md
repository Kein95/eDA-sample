# Đợt 2 — Đối soát sao kê

Phụ thuộc đợt 1. Edge function `eda-doi-soat`, tab mới trong `admin.html`.

## Nguyên tắc lấy từ VNCLO

Học nguyên hai điều đã chứng minh được là đúng ở `D:\Projects\VNCLO\vnclo`:

1. **Không bao giờ tự ghi tiền.** Upload chỉ trả về bản xem trước; người phụ trách tick
   rồi mới ghi. `admin.service.ts:154-234` làm đúng vậy.
2. **Dòng lệch tiền không được tick sẵn.** `Reconcile.tsx:28` chỉ preselect khi
   `amountOk`. Người vẫn xác nhận được, nhưng phải chủ động bấm.

Không lấy: parser hardcode layout Vietcombank, và việc không lưu giao dịch.

## Luồng

```
Upload .xlsx  ->  băm sha256
                    |
                    +-- trùng file đã upload  -> báo "file này đã xử lý ngày X", vẫn cho xem lại kết quả cũ
                    |
                    +-- file mới -> parse -> với mỗi dòng tiền vào:
                                              ma_gd đã có trong eda_bank_txn?
                                                 có   -> đánh dấu "đã xử lý trước", bỏ qua
                                                 chưa -> thử khớp -> ghi vào eda_bank_txn (chưa xác nhận)
                    |
                    v
              Bảng xem trước: Đã khớp / Chưa khớp / Đã xử lý trước
                    |
              người tick -> xác nhận -> set xac_nhan_boi, xac_nhan_luc + ghi eda_audit
```

Điểm khác VNCLO: giao dịch **được ghi vào DB ngay khi parse** (trạng thái chưa xác
nhận), không giữ trong RAM. Nhờ vậy `unique (ngan_hang, ma_gd)` mới phát huy tác dụng
và upload lại lần hai mới nhận ra được.

## Khớp giao dịch vào đợt nào

Đây là chỗ eDA khó hơn VNCLO. VNCLO chỉ cần tìm ra *người*; eDA còn phải biết là *đợt nào*.

1. Tìm người: regex `eDA26-[A-Z0-9]{6}` trong nội dung CK → nếu trượt, tìm `\b0\d{9}\b`
   đối chiếu `phone`. Ghi lại `khop_kieu`.
2. Tìm đợt: lấy đợt **chưa đóng đủ, thứ tự nhỏ nhất** của người đó.
3. So tiền:
   - đúng bằng số tiền đợt → khớp, tick sẵn
   - thiếu → khớp vào đợt đó nhưng **không tick sẵn**, hiện "thiếu N đồng"
   - thừa → khớp, hiện "thừa N đồng", không tick sẵn (có thể là đóng gộp 2 đợt, người
     phải tự quyết)

Cố ý không tự động chia một giao dịch cho nhiều đợt. Đoán sai ở đây là sai sổ tiền, mà
người phụ trách nhìn một giây là biết.

## Nội dung chuyển khoản

Theo VNCLO: `<mã đăng ký> <số điện thoại>` — hai khoá trong một chuỗi để regex bắt được
cả hai, phòng khi người gõ thiếu một. Chuỗi này phải **giống hệt nhau** ở ba nơi: trang
cảm ơn sau đăng ký, email xác nhận, và ảnh QR. Lệch một ký tự là khớp trượt.

## Định dạng sao kê

Không hardcode một ngân hàng. Tách thành `parsers/<ngan-hang>.ts`, mỗi parser trả về
mảng `{ma_gd, posted_at, so_tien, noi_dung}` chuẩn hoá. Bắt đầu bằng đúng một parser cho
ngân hàng eDA thật sự dùng **(chưa biết — câu hỏi 2 ở plan.md)**, nhưng đặt sẵn ranh
giới để thêm cái thứ hai không phải sửa lõi.

Nhận diện ngân hàng từ nội dung file, không tin phần mở rộng hay tên file.

## Việc phải làm

1. Edge function `eda-doi-soat`: nhận file, băm, parse, khớp, ghi giao dịch chưa xác nhận
2. Edge function `eda-xac-nhan-gd`: nhận danh sách id giao dịch, set xác nhận, ghi audit,
   kích hoạt email "đã nhận tiền"
3. Tab "Đối soát" trong `admin.html`: nút chọn file, 3 nhóm kết quả, nút xác nhận hàng loạt
4. Xuất danh sách chưa khớp ra `.xlsx` (VNCLO cố ý dùng xlsx thay CSV để không lỗi dấu
   tiếng Việt — giữ nguyên lựa chọn đó)

## Kiểm chứng

- **Upload cùng file hai lần → công nợ của mọi người không đổi.** Đây là test quan trọng
  nhất của cả kế hoạch.
- Hai file sao kê chồng lấn nhau (tháng 3 và quý 1) → giao dịch chung chỉ tính một lần
- Giao dịch thiếu tiền → không được tick sẵn
- Nội dung CK viết sai mã nhưng đúng SĐT → vẫn khớp, `khop_kieu = 'sdt'`
- Nội dung CK không có gì nhận ra được → vào nhóm chưa khớp, không ghi bừa vào ai
- Xác nhận xong → có dòng trong `eda_audit` kèm người bấm

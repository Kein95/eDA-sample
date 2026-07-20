# Brief: hoàn thiện giao diện điện thoại cho trang tuyển sinh eDA

Bản giao việc cho agent ngoài. Mọi số trong đây **đã đo trên trình duyệt thật**, không
phải suy từ đọc code. Đừng đo lại từ đầu, hãy dùng làm điểm xuất phát.

## Bối cảnh dự án

- File duy nhất cần sửa: `D:\Projects\eDA\TuyenSinh-eDA2026.dc.html` (~264KB, một file
  chứa cả trang). Không có bước build.
- Trang chạy bằng runtime DesignCombo (`support.js`): cú pháp `{{ }}`, `<sc-if>`,
  `<sc-for>`, và một class component ở cuối file. **Runtime dựng lại DOM mỗi lần đổi
  tab**, nên script kiểm tra phải chờ sau khi click tab.
- Style gần như toàn bộ nằm ở thuộc tính `style=` **inline**. Có một khối `<style>`
  chính bắt đầu ở khoảng dòng 49.
- **Mọi rule CSS ghi đè giá trị inline đều phải có `!important`.** Một số style còn do
  JS sinh ra lúc chạy (ví dụ `regGrid`). Đây là cái bẫy đã cắn nhiều lần ở repo này.

## Đã làm rồi, ĐỪNG làm lại

Trang vốn không có `@media` nào. Vừa thêm khối media query ĐẦU TIÊN (`max-width:700px`)
ngay sau `.glass-nav` trong khối `<style>`, giải quyết xong hai lỗi nặng:

1. **Dải tab biến mất trên điện thoại.** `nav` có 4 con, dải tab đặt `flex:1` nên là
   thứ duy nhất co được; logo 219px + nút giao diện 38px + nút CTA 143px đã vượt bề
   rộng máy, dải tab bị ép còn đúng 0px và cả 5 tab biến mất. Đã sửa: nav xuống hai
   hàng, dải tab `order:3; flex:1 0 100%`, ẩn pill, thu gọn thương hiệu và CTA.
2. **Trang cuộn ngang 55px ở mọi tab.** Do 7 lưới đặt tỉ lệ cứng không xuống một cột.
   Đã gắn class `co-doi-cot` cho 7 chỗ đó.

Kết quả hiện tại: `scrollWidth == clientWidth` ở cả 390 lẫn 360px, trên cả 7 tab.
Desktop 1440/768 không đổi một pixel.

## Việc cần làm

### 1. Thẻ tài liệu và thẻ giảng viên tràn nội bộ 10px

- Tab *Tài liệu*: 5 thẻ `a.scph`, mỗi thẻ `flex nowrap`, `scrollWidth - clientWidth = 10px`.
- Tab *Giảng viên*: 4 thẻ `div.scph` + 1 thẻ Mentors, cùng triệu chứng 10px.
- Không gây cuộn trang (bị cắt trong thẻ), nhưng nội dung mép phải bị xén.
- Gợi ý hướng: cho phép xuống dòng hoặc `min-width:0` cho phần chữ, đừng nới bề rộng thẻ.

### 2. Vài nhãn quá nhỏ trên điện thoại

| Chỗ | Cỡ hiện tại |
|---|---|
| Ký hiệu chú giải bảng ngành `● ◐ ○ ·` | 9px |
| `span.module-chip__label` ("MODULE 1") | 9.5px |
| `p.eyebrow`, `span.pill-tag`, nhãn thẻ tài liệu | 11 đến 11.5px |

Nâng tối thiểu 11px, ưu tiên 12px, **chỉ trong media query điện thoại**, đừng đụng desktop.

### 3. Bảng lịch học chật

`div.sched-row` dùng `grid-template-columns: 34px 56px 52px 1fr [auto]`. Ở 390px cột mô
tả chỉ còn ~102px. **KHÔNG được ép cả hàng xuống một cột dọc**: đây là bảng, làm vậy là
mất nghĩa hàng.

Hướng nên làm: trên điện thoại cho **phần mô tả xuống hàng riêng chiếm trọn bề ngang**,
còn ba cột đầu (số buổi, thứ, ngày) giữ nguyên trên một hàng. Mỗi buổi học vẫn là một
khối liền, mà mô tả được cả ~340px thay vì 102px. Kiểm cấu trúc DOM trước xem phần mô tả
có `grid-column: 1 / -1` được không.

**Hai cách KHÔNG nên làm, đã cân nhắc và loại:**

- *Chỉ thu hẹp hai cột đầu* (ví dụ `24px 46px 52px 1fr auto`): chỉ được thêm 20px, cột mô
  tả lên 122px, vẫn chật y như cũ. Tránh được rủi ro nhưng không giải quyết vấn đề.
- *Gắn `overflow-x:auto` thẳng vào `.sched-row`*: sai. Mỗi `.sched-row` là MỘT hàng, làm
  vậy thì **từng hàng cuộn ngang độc lập**, ra một cái bảng dùng không được. Nếu chọn
  hướng cuộn ngang thì phải gắn vào phần tử CHA bao toàn bộ các hàng, và phải kiểm xem
  thẻ cha đó có class định danh chưa.

## RÀNG BUỘC BẮT BUỘC

1. **Không đụng lưới `repeat(auto-fit, minmax(...))`** — chúng đã tự xuống dòng đúng.
2. **Không đụng dải ticker domain** (`flex nowrap` tràn 5232px). Đó là marquee chạy chữ
   cố ý, nằm trong `overflow:hidden`. Sửa là hỏng hiệu ứng.
3. **Không đổi bố cục desktop.** Mọi thay đổi nằm trong `@media (max-width:700px)`.
4. Chuỗi tiêu đề hero phải nằm trọn trong MỘT `<span>` và trùng khít `hero_tieu_de` ở
   khối JSON `#noi-dung-mac-dinh` cuối file. Lớp phủ CMS khớp chữ theo nguyên node; tách
   dòng là người vận hành mất khả năng sửa tiêu đề.
5. Đọc `README.md` mục **B9** trước khi đụng bất kỳ màu nào. Ở light mode các biến
   `--ink`, `--tintdeep`, `--deep` KHÔNG được đặt, mọi thứ chạy bằng giá trị dự phòng.

## Cách tự kiểm

Cần server xem thử và một Chrome mở cổng gỡ lỗi:

```bash
docker compose -f docker/docker-compose.yml up -d      # http://localhost:8791
chrome --remote-debugging-port=9222 --user-data-dir=<thư mục tạm>
```

Rồi chạy:

```bash
npm test                  # 74 kiểm tra, phải xanh hết
npm run test:trinh-duyet  # 53 kiểm tra trên trình duyệt thật
npm run build             # dựng bản deploy, báo lỗi nếu thiếu file
```

Tiêu chí đạt: `scrollWidth == clientWidth` ở 390 và 360px trên **cả 7 tab**, và ảnh chụp
1440px không khác gì trước khi sửa.

## Phân vai khi thực thi

- **Bạn chỉ sửa file, KHÔNG chạy lệnh.** Không chạy `npm`, không chạy test, không chạy
  `git` (không add, không commit, không pull, không checkout). Claude Code sẽ chạy toàn bộ
  phần kiểm tra bằng bộ đo trình duyệt đã dựng sẵn, rồi tự commit.
- **Chỉ được sửa một file:** `D:\Projects\eDA\TuyenSinh-eDA2026.dc.html`.
- Ưu tiên sửa **bên trong khối `@media (max-width: 700px)`** đã có sẵn trong khối
  `<style>`. Chỉ động vào HTML khi bắt buộc phải thêm class định danh, và khi đó nói rõ
  đã thêm class gì ở đâu.
- Xong thì liệt kê ngắn gọn: đã sửa những gì, ở dòng nào, và chỗ nào bạn không chắc.

Claude Code đã dừng sửa file này để nhường bạn, cây làm việc đang sạch ở commit mới nhất
của `master`.

# Đợt 1 — Schema học phí, đợt đóng, giao dịch ngân hàng

Migration mới: `0005_eda_hoc_phi.sql`, `0006_eda_giao_dich.sql`

## Vì sao không dùng một cột `payment_status`

VNCLO dùng `paymentStatus PENDING|APPROVED|REJECTED` và chạy được vì mỗi thí sinh trả
đúng một lần một khoản cố định. eDA theo kiểu AIO: 3 phương án, mỗi phương án 2–5 đợt,
số tiền và hạn khác nhau. Một enum không trả lời được "đã đóng đợt mấy, còn nợ bao
nhiêu, quá hạn đợt nào".

## Bảng

### `eda_payment_plan` — phương án học phí

```sql
create table public.eda_payment_plan (
  id          uuid primary key default gen_random_uuid(),
  code        text not null unique,          -- 'PA1', 'PA2', 'PA3'
  ten         text not null,                 -- 'Đóng 2 đợt — tổng 24 triệu'
  tong_tien   bigint not null check (tong_tien > 0),   -- VND, đơn vị đồng, KHÔNG dùng float
  mo_ta       text,
  dang_mo     boolean not null default true, -- đóng phương án cũ mà không xoá
  thu_tu      smallint not null default 0,
  created_at  timestamptz not null default now()
);
```

Tiền dùng `bigint` đơn vị đồng. Không `numeric`, không `float`: học phí Việt Nam là số
nguyên đồng, `float` sẽ sinh 23999999.999999997 khi cộng dồn các đợt.

### `eda_plan_installment` — các đợt của một phương án (bản mẫu)

```sql
create table public.eda_plan_installment (
  id          uuid primary key default gen_random_uuid(),
  plan_id     uuid not null references public.eda_payment_plan(id) on delete cascade,
  thu_tu      smallint not null,             -- 1, 2, 3...
  ten         text not null,                 -- 'Giữ chỗ', 'Trước khai giảng'
  so_tien     bigint not null check (so_tien > 0),
  han_dong    date,                          -- null = không có hạn cứng
  unique (plan_id, thu_tu)
);
```

Ràng buộc "tổng các đợt = tổng phương án" **không đặt được bằng CHECK** (liên bảng).
Đặt bằng trigger `after insert or update or delete` trên `eda_plan_installment`, hoặc
bằng một test chạy khi seed. Chọn trigger: sai lệch học phí là lỗi tiền, phải chặn ở DB.

### `eda_registration` — thêm cột

```sql
alter table public.eda_registration
  add column plan_id uuid references public.eda_payment_plan(id),
  add column trang_thai text not null default 'MOI'
      check (trang_thai in ('MOI','DA_XAC_NHAN','DANG_HOC','HUY')),
  add column ghi_chu_noi_bo text;   -- khác cột note (do người đăng ký gõ)
```

`plan_id` để null được: người đăng ký giữ chỗ trước, chọn phương án sau.

`trang_thai` ở đây là trạng thái **hồ sơ**, cố ý tách khỏi trạng thái **tiền**. Trạng
thái tiền suy ra từ các đợt đã đóng, không lưu trùng — lưu hai nơi là bảo đảm có ngày
lệch nhau.

### `eda_registration_installment` — đợt đóng của từng người

```sql
create table public.eda_registration_installment (
  id              uuid primary key default gen_random_uuid(),
  registration_id uuid not null references public.eda_registration(id) on delete cascade,
  thu_tu          smallint not null,
  ten             text not null,
  so_tien         bigint not null check (so_tien > 0),   -- đã trừ học bổng nếu có
  han_dong        date,
  mien_giam       bigint not null default 0 check (mien_giam >= 0),
  ly_do_mien_giam text,
  created_at      timestamptz not null default now(),
  unique (registration_id, thu_tu)
);
```

Vì sao sao chép ra thay vì trỏ thẳng vào `eda_plan_installment`: học bổng, giảm học
phí và gia hạn riêng cho từng người là chuyện có thật. Trỏ thẳng thì mọi ưu đãi cá nhân
đều phải sửa bản mẫu, ảnh hưởng người khác.

Sinh các dòng này khi gán `plan_id` — bằng function `eda_gan_phuong_an(reg_id, plan_id)`,
không phải bằng code ở client.

### `eda_bank_txn` — giao dịch ngân hàng

**Đây là bảng chặn đếm trùng.**

```sql
create table public.eda_bank_txn (
  id             uuid primary key default gen_random_uuid(),
  upload_id      uuid references public.eda_statement_upload(id) on delete set null,
  ma_gd          text not null,               -- số tham chiếu của ngân hàng
  ngan_hang      text not null,               -- 'VCB', 'TCB'...
  posted_at      timestamptz not null,
  so_tien        bigint not null,
  noi_dung       text not null,
  -- Kết quả khớp. Null = chưa khớp được vào ai.
  registration_id uuid references public.eda_registration(id) on delete set null,
  installment_id  uuid references public.eda_registration_installment(id) on delete set null,
  khop_kieu      text check (khop_kieu in ('ma','sdt','tay')),
  xac_nhan_boi   uuid references auth.users(id),
  xac_nhan_luc   timestamptz,
  created_at     timestamptz not null default now(),
  -- Cùng một giao dịch ngân hàng chỉ được tồn tại một lần, dù upload lại bao nhiêu lần.
  unique (ngan_hang, ma_gd)
);
```

`unique (ngan_hang, ma_gd)` là **thứ duy nhất** thực sự chặn đếm trùng. Không đặt niềm
tin vào việc "người dùng sẽ không upload lại file cũ" — họ sẽ upload lại.

Nếu sao kê của ngân hàng không có số tham chiếu, sinh khoá thay thế:
`ma_gd = encode(sha256(posted_at || so_tien || noi_dung), 'hex')`. Kém hơn mã thật (hai
giao dịch giống hệt nhau trong cùng một giây sẽ bị coi là một) nhưng vẫn tốt hơn không có.
Ghi rõ trong code là khoá thay thế.

### `eda_statement_upload` — lần upload sao kê

```sql
create table public.eda_statement_upload (
  id          uuid primary key default gen_random_uuid(),
  ten_file    text not null,
  sha256      text not null unique,      -- upload lại đúng file cũ thì nhận ra ngay
  ngan_hang   text not null,
  so_dong     integer not null,
  nguoi_upload uuid not null references auth.users(id),
  created_at  timestamptz not null default now()
);
```

`sha256` UNIQUE là lớp chặn thứ hai, ở mức file. Lớp thứ nhất là `ma_gd` ở mức giao dịch.
Cần cả hai: file khác nhau vẫn có thể chứa giao dịch trùng (sao kê tháng 3 và sao kê
quý 1 chồng nhau).

### `eda_audit` — nhật ký thao tác tiền

```sql
create table public.eda_audit (
  id          bigserial primary key,
  nguoi_dung  uuid references auth.users(id),
  hanh_dong   text not null,           -- 'xac_nhan_gd', 'gan_phuong_an', 'mien_giam'
  doi_tuong   text not null,           -- tên bảng + id
  chi_tiet    jsonb,
  created_at  timestamptz not null default now()
);
```

Không có audit thì không trả lời được "ai xác nhận khoản này" khi có tranh chấp tiền.

## View suy ra công nợ

```sql
create view public.eda_cong_no as
select r.id as registration_id,
       coalesce(sum(i.so_tien - i.mien_giam), 0)               as phai_dong,
       coalesce(sum(t.so_tien) filter (where t.xac_nhan_luc is not null), 0) as da_dong
  from public.eda_registration r
  left join public.eda_registration_installment i on i.registration_id = r.id
  left join public.eda_bank_txn t on t.installment_id = i.id
 group by r.id;
```

Chỉ cộng giao dịch **đã xác nhận**. Giao dịch khớp nhưng chưa ai bấm xác nhận không
được tính là đã thu.

## Việc phải làm

1. `0005_eda_hoc_phi.sql`: 4 bảng học phí + cột thêm vào `eda_registration` + trigger
   kiểm tổng + function `eda_gan_phuong_an`
2. `0006_eda_giao_dich.sql`: `eda_statement_upload`, `eda_bank_txn`, `eda_audit`, view
   `eda_cong_no`
3. RLS cho toàn bộ bảng mới — mặc định không policy, mở dần theo vai ở đợt 4
4. Seed phương án học phí thật **(đang chờ số liệu — xem câu hỏi 1 ở plan.md)**

## Kiểm chứng

- Chèn 3 phương án, mỗi phương án các đợt cộng lại **lệch** tổng → trigger phải chặn
- Gán phương án cho một đăng ký → sinh đúng số dòng đợt, đúng số tiền
- Chèn cùng `(ngan_hang, ma_gd)` hai lần → lần hai bị DB từ chối
- `eda_cong_no` với giao dịch chưa xác nhận → `da_dong` vẫn bằng 0

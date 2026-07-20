-- Hoc phi nhieu dot.
--
-- Vi sao khong dung mot cot payment_status: mot co true/false khong tra loi duoc "da
-- dong dot may, con no bao nhieu, qua han dot nao". VNCLO dung duoc mot enum chi vi moi
-- thi sinh tra dung mot lan mot khoan co dinh.
--
-- Tien dung bigint don vi DONG. Khong numeric, khong float: hoc phi Viet Nam la so
-- nguyen dong, va float se cho ra 23999999.999999997 khi cong don cac dot.

create table if not exists public.eda_payment_plan (
  id         uuid primary key default gen_random_uuid(),
  code       text not null unique,                      -- 'PA1', 'PA2', 'PA3'
  ten        text not null,
  tong_tien  bigint not null check (tong_tien > 0),
  mo_ta      text,
  dang_mo    boolean not null default true,             -- dong phuong an cu ma khong xoa
  thu_tu     smallint not null default 0,
  created_at timestamptz not null default now()
);

create table if not exists public.eda_plan_installment (
  id       uuid primary key default gen_random_uuid(),
  plan_id  uuid not null references public.eda_payment_plan(id) on delete cascade,
  thu_tu   smallint not null check (thu_tu > 0),
  ten      text not null,
  so_tien  bigint not null check (so_tien > 0),
  han_dong date,                                        -- null = khong co han cung
  unique (plan_id, thu_tu)
);

-- Tong cac dot phai bang tong phuong an.
-- Khong dat duoc bang CHECK vi rang buoc nay lien bang. Dat bang trigger chu khong phai
-- bang test luc seed: lech hoc phi la loi tien, phai chan o DB de moi duong ghi deu vuong.
create or replace function public.eda_kiem_tong_dot()
returns trigger
language plpgsql
as $$
declare
  v_plan uuid := coalesce(new.plan_id, old.plan_id);
  v_tong bigint;
  v_cong bigint;
begin
  select tong_tien into v_tong from public.eda_payment_plan where id = v_plan;
  if v_tong is null then return null; end if;      -- phuong an vua bi xoa cascade
  select coalesce(sum(so_tien), 0) into v_cong
    from public.eda_plan_installment where plan_id = v_plan;
  if v_cong <> v_tong then
    raise exception 'Tong cac dot (%) khac tong phuong an (%)', v_cong, v_tong;
  end if;
  return null;
end;
$$;

-- CONSTRAINT TRIGGER hoan den cuoi giao dich: chen 3 dot trong mot transaction thi sau
-- dong dau tien tong da khac roi, kiem ngay se bao loi oan.
drop trigger if exists eda_kiem_tong_dot_trg on public.eda_plan_installment;
create constraint trigger eda_kiem_tong_dot_trg
  after insert or update or delete on public.eda_plan_installment
  deferrable initially deferred
  for each row execute function public.eda_kiem_tong_dot();

-- ── Gan phuong an cho tung nguoi ──────────────────────────────────────────
alter table public.eda_registration
  add column if not exists plan_id uuid references public.eda_payment_plan(id),
  add column if not exists trang_thai text not null default 'MOI',
  add column if not exists ghi_chu_noi_bo text;          -- khac cot note (nguoi dang ky go)

do $$ begin
  alter table public.eda_registration
    add constraint eda_registration_trang_thai_chk
    check (trang_thai in ('MOI','DA_XAC_NHAN','DANG_HOC','HUY'));
exception when duplicate_object then null; end $$;

-- trang_thai o day la trang thai HO SO. Co y tach khoi trang thai TIEN: trang thai tien
-- suy ra tu cac dot da thu (view eda_cong_no o 0006), khong luu trung. Luu hai noi la
-- bao dam co ngay hai noi lech nhau.

create table if not exists public.eda_registration_installment (
  id              uuid primary key default gen_random_uuid(),
  registration_id uuid not null references public.eda_registration(id) on delete cascade,
  thu_tu          smallint not null check (thu_tu > 0),
  ten             text not null,
  so_tien         bigint not null check (so_tien > 0),
  han_dong        date,
  mien_giam       bigint not null default 0 check (mien_giam >= 0),
  ly_do_mien_giam text,
  created_at      timestamptz not null default now(),
  unique (registration_id, thu_tu),
  -- Mien giam khong duoc vuot so tien dot: am tien la vo nghia va se lam view cong no
  -- ra so am, ke toan doi chieu khong hieu tu dau ra.
  constraint eda_mien_giam_khong_vuot check (mien_giam <= so_tien)
);

create index if not exists eda_reg_installment_reg_idx
  on public.eda_registration_installment (registration_id, thu_tu);

-- Sao chep tu ban mau ra thay vi tro thang vao eda_plan_installment: hoc bong, giam hoc
-- phi va gia han rieng cho tung nguoi la chuyen co that. Tro thang thi moi uu dai ca
-- nhan deu phai sua ban mau, anh huong nguoi khac.
create or replace function public.eda_gan_phuong_an(p_reg uuid, p_plan uuid)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare n integer;
begin
  -- Da thu tien roi thi khong cho doi phuong an: cac dot cu bi xoa se keo theo lien ket
  -- giao dich, tien da nhan thanh khong gan vao dau.
  if exists (
    select 1 from public.eda_bank_txn t
      join public.eda_registration_installment i on i.id = t.installment_id
     where i.registration_id = p_reg and t.xac_nhan_luc is not null
  ) then
    raise exception 'Da co giao dich duoc xac nhan, khong doi phuong an duoc. Huy xac nhan truoc.';
  end if;

  delete from public.eda_registration_installment where registration_id = p_reg;

  insert into public.eda_registration_installment (registration_id, thu_tu, ten, so_tien, han_dong)
  select p_reg, thu_tu, ten, so_tien, han_dong
    from public.eda_plan_installment where plan_id = p_plan;
  get diagnostics n = row_count;

  update public.eda_registration set plan_id = p_plan where id = p_reg;
  return n;
end;
$$;

-- RLS: bat, KHONG policy nao o day. Quyen mo dan o 0007 theo tung vai.
alter table public.eda_payment_plan            enable row level security;
alter table public.eda_plan_installment        enable row level security;
alter table public.eda_registration_installment enable row level security;

-- Chua co hoc phi that (chua chot so, chua chon ngan hang) nen KHONG seed phuong an nao.
-- Co y khong dien so gia cho "co du lieu ma chay thu": so gia trong bang tien la thu se
-- co nguoi tuong that. Xem plans/260720-0904-backend-dang-ky-doi-soat-cms/plan.md.

-- Giao dich ngan hang + nhat ky thao tac.

create table if not exists public.eda_statement_upload (
  id           uuid primary key default gen_random_uuid(),
  ten_file     text not null,
  -- Bam noi dung file. UNIQUE de upload lai DUNG file cu thi nhan ra ngay, khoi bat
  -- nguoi dung ngoi doi doi soat lai tu dau.
  sha256       text not null unique,
  ngan_hang    text not null,
  so_dong      integer not null,
  nguoi_upload uuid not null references auth.users(id),
  created_at   timestamptz not null default now()
);

create table if not exists public.eda_bank_txn (
  id              uuid primary key default gen_random_uuid(),
  upload_id       uuid references public.eda_statement_upload(id) on delete set null,
  ma_gd           text not null,                -- so tham chieu cua ngan hang
  ma_la_thay_the  boolean not null default false, -- true = tu bam ra vi sao ke khong co ma
  ngan_hang       text not null,
  posted_at       timestamptz not null,
  so_tien         bigint not null check (so_tien > 0),
  noi_dung        text not null,

  registration_id uuid references public.eda_registration(id) on delete set null,
  installment_id  uuid references public.eda_registration_installment(id) on delete set null,
  khop_kieu       text check (khop_kieu in ('ma','sdt','tay')),
  xac_nhan_boi    uuid references auth.users(id),
  xac_nhan_luc    timestamptz,
  created_at      timestamptz not null default now(),

  -- ĐÂY la thu that su chan dem tien hai lan. Khong dat niem tin vao viec "nguoi dung
  -- se khong upload lai file cu" - ho se upload lai. Cung khong dat niem tin vao doan
  -- loc o client (locGiaoDichMoi): no chay trong trinh duyet, ai cung sua duoc.
  unique (ngan_hang, ma_gd),

  -- Da xac nhan thi phai biet ai xac nhan va gan vao dot nao. Khong cho ton tai trang
  -- thai "da thu tien nhung khong biet cua ai".
  constraint eda_txn_xac_nhan_du_thong_tin check (
    xac_nhan_luc is null
    or (xac_nhan_boi is not null and installment_id is not null)
  )
);

create index if not exists eda_bank_txn_chua_khop_idx
  on public.eda_bank_txn (created_at desc) where registration_id is null;
create index if not exists eda_bank_txn_dot_idx
  on public.eda_bank_txn (installment_id) where xac_nhan_luc is not null;

-- ── Cong no: suy ra, khong luu ─────────────────────────────────────────────
-- Chi cong giao dich DA XAC NHAN. Giao dich khop nhung chua ai bam xac nhan khong duoc
-- tinh la da thu - do moi la de xuat cua may, chua phai quyet dinh cua nguoi.
create or replace view public.eda_cong_no as
select r.id as registration_id,
       coalesce(sum(distinct_i.can_thu), 0) as phai_dong,
       coalesce((
         select sum(t.so_tien) from public.eda_bank_txn t
           join public.eda_registration_installment i2 on i2.id = t.installment_id
          where i2.registration_id = r.id and t.xac_nhan_luc is not null
       ), 0) as da_dong
  from public.eda_registration r
  left join lateral (
    select sum(i.so_tien - i.mien_giam) as can_thu
      from public.eda_registration_installment i
     where i.registration_id = r.id
  ) distinct_i on true
 group by r.id, distinct_i.can_thu;

-- ── Nhat ky thao tac ───────────────────────────────────────────────────────
-- Yeu cau: MOI thao tac deu phai co log.
--
-- Lam bang trigger o DB chu khong phai bang code ung dung. Ly do: code ung dung co
-- nhieu duong vao (edge function, SQL editor cua Supabase, script vet), quen ghi log o
-- mot duong la mat dau vet ma khong ai biet. Trigger thi moi duong ghi deu di qua.
create table if not exists public.eda_audit (
  id         bigserial primary key,
  nguoi_dung uuid,                    -- null = service-role hoac cron, van phai ghi lai
  hanh_dong  text not null,           -- INSERT | UPDATE | DELETE
  bang       text not null,
  ban_ghi    uuid,
  truoc      jsonb,
  sau        jsonb,
  created_at timestamptz not null default now()
);

create index if not exists eda_audit_bang_idx on public.eda_audit (bang, created_at desc);
create index if not exists eda_audit_nguoi_idx on public.eda_audit (nguoi_dung, created_at desc);

create or replace function public.eda_ghi_log()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  v_id uuid;
begin
  v_id := case when tg_op = 'DELETE' then (to_jsonb(old) ->> 'id')::uuid
                                     else (to_jsonb(new) ->> 'id')::uuid end;
  insert into public.eda_audit (nguoi_dung, hanh_dong, bang, ban_ghi, truoc, sau)
  values (auth.uid(), tg_op, tg_table_name, v_id,
          case when tg_op = 'INSERT' then null else to_jsonb(old) end,
          case when tg_op = 'DELETE' then null else to_jsonb(new) end);
  return null;
end;
$$;

do $$
declare b text;
begin
  foreach b in array array[
    'eda_registration', 'eda_registration_installment',
    'eda_payment_plan', 'eda_plan_installment',
    'eda_bank_txn', 'eda_statement_upload'
  ] loop
    execute format('drop trigger if exists eda_log_trg on public.%I', b);
    execute format(
      'create trigger eda_log_trg after insert or update or delete on public.%I
         for each row execute function public.eda_ghi_log()', b);
  end loop;
end $$;

-- Nhat ky khong duoc sua, khong duoc xoa - ke ca boi admin. Mot nhat ky chinh sua duoc
-- thi khong con la bang chung, va gia tri duy nhat cua no la lam bang chung.
alter table public.eda_audit enable row level security;
revoke insert, update, delete on public.eda_audit from anon, authenticated;
-- Trigger ghi duoc vi ham eda_ghi_log() la security definer, chay quyen chu so huu.

alter table public.eda_statement_upload enable row level security;
alter table public.eda_bank_txn          enable row level security;

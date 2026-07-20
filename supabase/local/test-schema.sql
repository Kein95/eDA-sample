-- Kiem cac rang buoc cua schema eDA bang du lieu that.
--
--   bash scripts/test-db.sh
--
-- Moi kiem tra deu phai CHUNG MINH duoc rang buoc that su chan, chu khong phai chi
-- chay khong loi. Mot rang buoc chi "co trong file" ma khong chan gi thi vo dung.
\set ON_ERROR_STOP on
\set QUIET on
-- notice chu khong phai warning: cac dong "ok" bao dat deu la RAISE NOTICE, dat muc
-- warning la nuot het va test chay xong khong in gi.
set client_min_messages = notice;
-- Bo phan in ket qua tra ve cua ham (nhung dong "(1 row)" rong) cho de doc.
\pset tuples_only on
\pset format unaligned

create or replace function pg_temp.dat(ten text) returns void
language plpgsql as $$ begin raise notice '  ok  %', ten; end $$;

-- Chay mot cau lenh va doi no PHAI hong. Hong dung la dat.
create or replace function pg_temp.phai_hong(ten text, lenh text) returns void
language plpgsql as $$
begin
  begin
    execute lenh;
    -- Trigger kiem tong dot dat "initially deferred" nen binh thuong chi no luc COMMIT,
    -- tuc la sau khi khoi exception nay da ket thuc va ham da ket luan "chay duoc".
    -- Ep kiem ngay tai day de rang buoc hoan lai cung kiem duoc that.
    set constraints all immediate;
  exception when others then
    raise notice '  ok  % (bi chan: %)', ten, left(replace(sqlerrm, E'\n', ' '), 60);
    return;
  end;
  raise exception 'THAT BAI: % - lenh chay duoc trong khi phai bi chan', ten;
end $$;

-- ── 1. Tong cac dot phai bang tong phuong an ───────────────────────────────
insert into eda_payment_plan (id, code, ten, tong_tien) values
  ('11111111-1111-1111-1111-111111111111', 'PA1', 'Hai dot',  24000000),
  ('22222222-2222-2222-2222-222222222222', 'PA2', 'Ba dot',   26000000);

do $$ begin
  insert into eda_plan_installment (plan_id, thu_tu, ten, so_tien) values
    ('11111111-1111-1111-1111-111111111111', 1, 'Giu cho',  4000000),
    ('11111111-1111-1111-1111-111111111111', 2, 'Truoc KG', 20000000);
  perform pg_temp.dat('tong cac dot = tong phuong an thi chen duoc');
end $$;

select pg_temp.phai_hong(
  'tong cac dot LECH thi bi chan',
  $$insert into eda_plan_installment (plan_id, thu_tu, ten, so_tien) values
      ('22222222-2222-2222-2222-222222222222', 1, 'Sai tong', 1000000)$$);

-- Trigger phai la deferred: chen 3 dot trong mot giao dich thi sau dong dau tong da
-- lech, kiem ngay se bao loi oan.
do $$ begin
  insert into eda_plan_installment (plan_id, thu_tu, ten, so_tien) values
    ('22222222-2222-2222-2222-222222222222', 1, 'Giu cho',  4000000),
    ('22222222-2222-2222-2222-222222222222', 2, 'Dot 2',   12000000),
    ('22222222-2222-2222-2222-222222222222', 3, 'Dot 3',   10000000);
  perform pg_temp.dat('chen nhieu dot trong mot giao dich khong bao loi oan');
end $$;

-- ── 2. Gan phuong an sinh dung cac dot ─────────────────────────────────────
insert into auth.users (id, email) values
  ('aaaaaaaa-0000-0000-0000-000000000001', 'admin@eda.test'),
  ('aaaaaaaa-0000-0000-0000-000000000002', 'ketoan@eda.test'),
  ('aaaaaaaa-0000-0000-0000-000000000003', 'trogiang@eda.test');

insert into eda_registration (id, code, name, phone, email, guardian_phone) values
  ('bbbbbbbb-0000-0000-0000-000000000001', 'eDA26-ABC123', 'Nguyen Van A', '0900000001', 'a@example.com', '0911111111');

do $$
declare n integer;
begin
  n := eda_gan_phuong_an('bbbbbbbb-0000-0000-0000-000000000001',
                         '22222222-2222-2222-2222-222222222222');
  if n <> 3 then raise exception 'THAT BAI: sinh % dot, mong doi 3', n; end if;
  perform pg_temp.dat('gan phuong an sinh dung 3 dot');
end $$;

select pg_temp.phai_hong(
  'mien giam vuot so tien dot thi bi chan',
  $$update eda_registration_installment set mien_giam = 999999999
     where registration_id = 'bbbbbbbb-0000-0000-0000-000000000001' and thu_tu = 1$$);

-- ── 3. Chong dem tien hai lan ──────────────────────────────────────────────
insert into eda_statement_upload (id, ten_file, sha256, ngan_hang, so_dong, nguoi_upload)
values ('cccccccc-0000-0000-0000-000000000001', 'saoke-t7.csv', 'bam-1', 'VCB', 5,
        'aaaaaaaa-0000-0000-0000-000000000002');

insert into eda_bank_txn (upload_id, ma_gd, ngan_hang, posted_at, so_tien, noi_dung)
values ('cccccccc-0000-0000-0000-000000000001', 'GD001', 'VCB', now(), 4000000, 'eDA26-ABC123');
select pg_temp.dat('chen giao dich lan dau: duoc');

select pg_temp.phai_hong(
  'CHEN LAI CUNG MA GIAO DICH bi chan (day la thu chan dem tien hai lan)',
  $$insert into eda_bank_txn (ma_gd, ngan_hang, posted_at, so_tien, noi_dung)
    values ('GD001', 'VCB', now(), 4000000, 'eDA26-ABC123')$$);

do $$ begin
  insert into eda_bank_txn (ma_gd, ngan_hang, posted_at, so_tien, noi_dung)
  values ('GD001', 'TCB', now(), 4000000, 'ngan hang khac');
  perform pg_temp.dat('cung ma nhung KHAC ngan hang thi van chen duoc');
end $$;

select pg_temp.phai_hong(
  'upload lai dung file cu bi chan boi sha256 unique',
  $$insert into eda_statement_upload (ten_file, sha256, ngan_hang, so_dong, nguoi_upload)
    values ('saoke-t7-copy.csv', 'bam-1', 'VCB', 5, 'aaaaaaaa-0000-0000-0000-000000000002')$$);

select pg_temp.phai_hong(
  'xac nhan ma khong gan vao dot nao thi bi chan',
  $$update eda_bank_txn set xac_nhan_luc = now(),
       xac_nhan_boi = 'aaaaaaaa-0000-0000-0000-000000000002'
     where ma_gd = 'GD001' and ngan_hang = 'VCB'$$);

-- ── 4. Cong no chi tinh giao dich DA XAC NHAN ──────────────────────────────
do $$
declare v_dot uuid; v_phai bigint; v_da bigint;
begin
  select id into v_dot from eda_registration_installment
   where registration_id = 'bbbbbbbb-0000-0000-0000-000000000001' and thu_tu = 1;

  update eda_bank_txn set installment_id = v_dot, khop_kieu = 'ma'
   where ma_gd = 'GD001' and ngan_hang = 'VCB';

  select phai_dong, da_dong into v_phai, v_da from eda_cong_no
   where registration_id = 'bbbbbbbb-0000-0000-0000-000000000001';
  if v_phai <> 26000000 then raise exception 'THAT BAI: phai_dong = %, mong doi 26000000', v_phai; end if;
  if v_da <> 0 then raise exception 'THAT BAI: khop nhung CHUA xac nhan ma da_dong = %', v_da; end if;
  perform pg_temp.dat('khop nhung chua xac nhan: da_dong van bang 0');

  update eda_bank_txn set xac_nhan_luc = now(),
         xac_nhan_boi = 'aaaaaaaa-0000-0000-0000-000000000002'
   where ma_gd = 'GD001' and ngan_hang = 'VCB';

  select da_dong into v_da from eda_cong_no
   where registration_id = 'bbbbbbbb-0000-0000-0000-000000000001';
  if v_da <> 4000000 then raise exception 'THAT BAI: sau xac nhan da_dong = %, mong doi 4000000', v_da; end if;
  perform pg_temp.dat('sau khi xac nhan: da_dong = 4.000.000');
end $$;

select pg_temp.phai_hong(
  'da co giao dich xac nhan thi khong doi phuong an duoc',
  $$select eda_gan_phuong_an('bbbbbbbb-0000-0000-0000-000000000001',
                             '11111111-1111-1111-1111-111111111111')$$);

-- ── 5. Nhat ky ghi day du ──────────────────────────────────────────────────
do $$
declare n integer;
begin
  select count(*) into n from eda_audit where bang = 'eda_bank_txn';
  -- 2 INSERT (VCB, TCB) + 2 UPDATE (khop, xac nhan)
  if n < 4 then raise exception 'THAT BAI: chi co % dong log cho eda_bank_txn, mong doi >= 4', n; end if;
  perform pg_temp.dat(format('nhat ky ghi du thao tac tren giao dich (%s dong)', n));

  select count(*) into n from eda_audit where bang = 'eda_registration_installment';
  if n < 3 then raise exception 'THAT BAI: khong ghi log khi sinh cac dot'; end if;
  perform pg_temp.dat(format('nhat ky ghi ca viec sinh cac dot (%s dong)', n));

  select count(*) into n from eda_audit
   where bang = 'eda_bank_txn' and hanh_dong = 'UPDATE' and sau ->> 'xac_nhan_luc' is not null;
  if n < 1 then raise exception 'THAT BAI: khong ghi lai noi dung sau khi xac nhan'; end if;
  perform pg_temp.dat('nhat ky luu ca gia tri truoc va sau');
end $$;

\echo ''
\echo 'Tat ca kiem tra schema deu dat.'

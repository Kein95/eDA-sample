-- Kiem phan quyen bang cach GIA LAP dang nhap tung vai roi goi that.
--
-- Kiem o tang CSDL chu khong phai o tang giao dien: an nut tren trang admin khong phai
-- la phan quyen, ai cung goi thang REST API duoc. Cho nen moi test o day deu chay
-- "set role authenticated" + dat claim JWT y nhu PostgREST lam.
--
-- Chay sau test-schema.sql (dung du lieu no da tao).
\set ON_ERROR_STOP on
\set QUIET on
set client_min_messages = notice;
\pset tuples_only on
\pset format unaligned

-- Dang nhap gia: dat claim y nhu PostgREST dat truoc moi truy van.
create or replace function pg_temp.dang_nhap(vai text, uid uuid) returns void
language plpgsql as $$
begin
  perform set_config('request.jwt.claims',
    json_build_object('sub', uid, 'app_metadata', json_build_object('role', vai))::text, true);
end $$;

create or replace function pg_temp.dat(ten text) returns void
language plpgsql as $$ begin raise notice '  ok  %', ten; end $$;

create or replace function pg_temp.phai_hong(ten text, lenh text) returns void
language plpgsql as $$
begin
  begin
    execute lenh;
    set constraints all immediate;
  exception when others then
    raise notice '  ok  % (bi chan: %)', ten, left(replace(sqlerrm, E'\n', ' '), 55);
    return;
  end;
  raise exception 'THAT BAI: % - lam duoc trong khi phai bi chan', ten;
end $$;

-- RLS tu choi GHI bang cach sua 0 dong, cung khong bao loi. Con quyen o muc cot thi
-- bao loi that. Hai co che khac nhau nen phai chap nhan ca hai, va phai kiem SO DONG
-- BI TAC DONG - "khong bao loi" khong phai bang chung la da chan.
create or replace function pg_temp.phai_khong_doi(ten text, lenh text) returns void
language plpgsql as $$
declare n integer;
begin
  begin
    execute lenh;
    get diagnostics n = row_count;
  exception when others then
    raise notice '  ok  % (bi chan: %)', ten, left(replace(sqlerrm, E'\n', ' '), 50);
    return;
  end;
  if n <> 0 then
    raise exception 'THAT BAI: % - sua duoc % dong, phai la 0', ten, n;
  end if;
  raise notice '  ok  % (RLS loc het, 0 dong bi sua)', ten;
end $$;

-- RLS tu choi DOC bang cach loc het dong di, KHONG bang cach bao loi. Dung phai_hong()
-- cho mot cau SELECT la kiem rong tuech: cau lenh luon "chay duoc", chi la tra ve 0
-- dong, nen test nao cung dat du policy co sai. Doc thi phai dem dong.
create or replace function pg_temp.phai_rong(ten text, cau_dem text) returns void
language plpgsql as $$
declare n bigint;
begin
  begin
    execute cau_dem into n;
  exception when insufficient_privilege then
    raise notice '  ok  % (chan o muc quyen bang)', ten;
    return;
  end;
  if n <> 0 then
    raise exception 'THAT BAI: % - doc duoc % dong, phai la 0', ten, n;
  end if;
  raise notice '  ok  % (RLS loc het, 0 dong)', ten;
end $$;

-- ── Tro giang ──────────────────────────────────────────────────────────────
begin;
set local role authenticated;
select pg_temp.dang_nhap('EDA_TA', 'aaaaaaaa-0000-0000-0000-000000000003');

do $$
declare n integer; v_du integer;
begin
  select count(*) into n from eda_registration_tro_giang;
  if n < 1 then raise exception 'THAT BAI: tro giang khong doc duoc view cua chinh minh'; end if;
  perform pg_temp.dat(format('tro giang doc duoc danh sach hoc vien (%s dong)', n));

  -- da_dong_du tinh thang tu bang goc chu khong qua view eda_cong_no (view do da chan lai
  -- cho vai dung tien). Di qua no thi cot nay im lang thanh null va tro giang mat het thong
  -- tin ai da dong du - hong ma khong bao gi.
  select count(*) into v_du from eda_registration_tro_giang where da_dong_du is not null;
  if v_du <> n then
    raise exception 'THAT BAI: % / % dong co da_dong_du la null', n - v_du, n;
  end if;
  perform pg_temp.dat('tro giang van thay duoc da_dong_du (boolean, khong phai so tien)');
end $$;

-- Cot nhay cam khong duoc co trong view. Kiem bang cach GOI THAT, khong phai bang
-- cach doc dinh nghia view: dinh nghia doc duoc ma quyen sai thi van lo du lieu.
select pg_temp.phai_hong(
  'tro giang KHONG lay duoc SDT phu huynh qua view',
  $$select guardian_phone from eda_registration_tro_giang limit 1$$);

-- Kiem CA BANG GOC, khong chi cai view.
--
-- Ban truoc chi kiem view roi ket luan la kin, trong khi bang goc van mo: tro giang goi
-- thang REST vao eda_registration la lay duoc guardian_phone. Che mot cua ma khong kiem
-- cua con lai thi bo kiem chi chung minh duoc rang cua da che thi da che.
select pg_temp.phai_rong(
  'tro giang KHONG doc duoc BANG GOC eda_registration',
  $$select count(*) from eda_registration$$);

select pg_temp.phai_rong(
  'tro giang KHONG lay duoc SDT phu huynh THANG TU BANG GOC',
  $$select count(guardian_phone) from eda_registration$$);

select pg_temp.phai_rong(
  'tro giang KHONG doc duoc giao dich ngan hang',
  $$select count(*) from eda_bank_txn$$);

select pg_temp.phai_rong(
  'tro giang KHONG doc duoc cac dot dong tien',
  $$select count(*) from eda_registration_installment$$);

-- Nhat ky chua ban chup truoc/sau duoi dang jsonb, tuc la chua ca SDT phu huynh va so
-- tien. Doc duoc nhat ky la di duong vong qua dung cac cot bi cam xem.
select pg_temp.phai_rong(
  'tro giang KHONG doc duoc nhat ky',
  $$select count(*) from eda_audit$$);

select pg_temp.phai_rong(
  'tro giang KHONG doc duoc so tien qua view cong no',
  $$select count(*) from eda_cong_no$$);

select pg_temp.phai_hong(
  'tro giang KHONG goi duoc ham gan phuong an',
  $$select eda_gan_phuong_an('bbbbbbbb-0000-0000-0000-000000000001', null)$$);

select pg_temp.phai_khong_doi(
  'tro giang KHONG sua duoc don dang ky',
  $$update eda_registration set name = 'bi doi ten' where code = 'eDA26-ABC123'$$);
commit;

-- ── Ke toan ────────────────────────────────────────────────────────────────
begin;
set local role authenticated;
select pg_temp.dang_nhap('EDA_ACCOUNTANT', 'aaaaaaaa-0000-0000-0000-000000000002');

do $$
declare n integer;
begin
  select count(*) into n from eda_bank_txn;
  if n < 1 then raise exception 'THAT BAI: ke toan khong doc duoc giao dich'; end if;
  perform pg_temp.dat(format('ke toan doc duoc giao dich ngan hang (%s dong)', n));

  update eda_bank_txn set khop_kieu = 'tay' where ngan_hang = 'TCB';
  perform pg_temp.dat('ke toan KHOP duoc giao dich (cot khop_kieu)');
end $$;

-- Day la ranh gioi quan trong nhat: ke toan ghi nhan tien VAO, admin quyet dinh PHAI
-- THU bao nhieu. Neu mot tai khoan lam duoc ca hai thi mien giam khong roi khop cho
-- khop so la thao tac khong ai phat hien duoc.
select pg_temp.phai_khong_doi(
  'ke toan KHONG sua duoc so tien cua giao dich',
  $$update eda_bank_txn set so_tien = 1 where ngan_hang = 'TCB'$$);

select pg_temp.phai_khong_doi(
  'ke toan KHONG sua duoc noi dung chuyen khoan',
  $$update eda_bank_txn set noi_dung = 'sua cho vua' where ngan_hang = 'TCB'$$);

select pg_temp.phai_khong_doi(
  'ke toan KHONG mien giam duoc',
  $$update eda_registration_installment set mien_giam = 1000000 where thu_tu = 2$$);

select pg_temp.phai_khong_doi(
  'ke toan KHONG sua duoc don dang ky',
  $$update eda_registration set phone = '0999999999' where code = 'eDA26-ABC123'$$);

select pg_temp.phai_khong_doi(
  'ke toan KHONG doi duoc hoc phi cua phuong an',
  $$update eda_payment_plan set tong_tien = 1 where code = 'PA1'$$);

select pg_temp.phai_rong(
  'ke toan KHONG doc duoc nhat ky',
  $$select count(*) from eda_audit$$);

select pg_temp.phai_khong_doi(
  'ke toan KHONG xac nhan ho nguoi khac duoc',
  $$update eda_bank_txn
       set xac_nhan_luc = now(), xac_nhan_boi = 'aaaaaaaa-0000-0000-0000-000000000001'
     where ngan_hang = 'TCB'$$);

-- Chan duong UPDATE ma khong chan duong INSERT thi ke toan chen thang mot dong da danh
-- dau "admin da xac nhan", va nhat ky se ghi rang admin duyet khoan tien do.
select pg_temp.phai_hong(
  'ke toan KHONG CHEN duoc giao dich mang ten nguoi khac',
  $$insert into eda_bank_txn (ngan_hang, ma_gd, posted_at, so_tien, noi_dung,
                              xac_nhan_luc, xac_nhan_boi)
    values ('VCB', 'GIA-MAO-1', now(), 1000, 'thu chen ho',
            now(), 'aaaaaaaa-0000-0000-0000-000000000001')$$);

select pg_temp.phai_hong(
  'ke toan KHONG goi duoc ham gan phuong an',
  $$select eda_gan_phuong_an('bbbbbbbb-0000-0000-0000-000000000001', null)$$);
commit;

-- ── Admin ──────────────────────────────────────────────────────────────────
begin;
set local role authenticated;
select pg_temp.dang_nhap('EDA_ADMIN', 'aaaaaaaa-0000-0000-0000-000000000001');

do $$ begin
  update eda_registration_installment set mien_giam = 1000000, ly_do_mien_giam = 'hoc bong'
   where registration_id = 'bbbbbbbb-0000-0000-0000-000000000001' and thu_tu = 2;
  perform pg_temp.dat('admin mien giam duoc');

  update eda_registration set ghi_chu_noi_bo = 'da goi dien' where code = 'eDA26-ABC123';
  perform pg_temp.dat('admin sua duoc don dang ky');
end $$;

do $$
declare n integer; v jsonb;
begin
  select count(*) into n from eda_audit;
  if n < 1 then raise exception 'THAT BAI: admin khong doc duoc nhat ky - nhat ky khong doc duoc thi vo dung'; end if;
  perform pg_temp.dat(format('admin DOC duoc nhat ky (%s dong)', n));

  -- 0004 xoa don dang ky sau 24 thang, nhung nhat ky khong co han luu. Ghi nguyen ban ghi
  -- vao day tuc la chinh sach luu tru chi DI DOI so dien thoai sang mot bang vinh vien.
  update eda_registration set ghi_chu_noi_bo = 'kiem che pii' where code = 'eDA26-ABC123';
  select sau into v from eda_audit
   where bang = 'eda_registration' order by created_at desc limit 1;
  if v ->> 'phone' is distinct from '(đã che)' then
    raise exception 'THAT BAI: nhat ky luu nguyen SDT hoc vien: %', v ->> 'phone';
  end if;
  if v ->> 'guardian_phone' is not null and v ->> 'guardian_phone' <> '(đã che)' then
    raise exception 'THAT BAI: nhat ky luu nguyen SDT phu huynh: %', v ->> 'guardian_phone';
  end if;
  if v ->> 'code' is null then
    raise exception 'THAT BAI: che qua tay, mat luon cot khong nhay cam';
  end if;
  perform pg_temp.dat('nhat ky CHE thong tin ca nhan, van giu cot de doi chieu');
end $$;

do $$
declare v_phai bigint;
begin
  select phai_dong into v_phai from eda_cong_no
   where registration_id = 'bbbbbbbb-0000-0000-0000-000000000001';
  if v_phai <> 25000000 then raise exception 'THAT BAI: sau mien giam 1tr, phai_dong = %', v_phai; end if;
  perform pg_temp.dat('mien giam 1tr -> phai_dong tu 26tr xuong 25tr');
end $$;
commit;

-- ── Khong dang nhap ────────────────────────────────────────────────────────
begin;
set local role anon;
select pg_temp.phai_rong('nguoi la KHONG doc duoc don dang ky',
                         $$select count(*) from eda_registration$$);
-- View chay bang quyen nguoi tao nen KHONG bi RLS chan. Cong duy nhat cua no la menh de
-- where trong chinh view, va grant chi cap cho authenticated. Phai kiem that.
select pg_temp.phai_rong('nguoi la KHONG doc duoc view cua tro giang',
                         $$select count(*) from eda_registration_tro_giang$$);
select pg_temp.phai_rong('nguoi la KHONG doc duoc giao dich',
                         $$select count(*) from eda_bank_txn$$);
select pg_temp.phai_rong('nguoi la KHONG doc duoc nhat ky',
                         $$select count(*) from eda_audit$$);

-- View KHONG bat security_invoker thi chay bang quyen chu so huu va bo qua RLS cua bang
-- duoi. Bang goc kin ma view ho la nguoi la cam anon key doc duoc het so tien. Bang goc
-- kin roi khong co nghia la view kin.
select pg_temp.phai_rong('nguoi la KHONG doc duoc cong no qua view',
                         $$select count(*) from eda_cong_no$$);
select pg_temp.phai_rong('nguoi la KHONG doc duoc bang gia hoc phi',
                         $$select count(*) from eda_payment_plan$$);
select pg_temp.phai_rong('nguoi la KHONG doc duoc noi dung trang',
                         $$select count(*) from eda_noi_dung$$);

-- Ham security definer bo qua RLS. Khong revoke va khong tu kiem vai thi PostgREST bay no
-- thanh mot endpoint /rpc/... goi duoc bang anon key cong khai.
select pg_temp.phai_hong(
  'nguoi la KHONG goi duoc ham gan phuong an',
  $$select eda_gan_phuong_an('bbbbbbbb-0000-0000-0000-000000000001', null)$$);
commit;

-- ── Noi dung trang ─────────────────────────────────────────────────────────
begin;
set local role authenticated;
select pg_temp.dang_nhap('EDA_ADMIN', 'aaaaaaaa-0000-0000-0000-000000000001');

do $$
declare v text;
begin
  insert into eda_noi_dung (khoa, loai, gia_tri, mo_ta)
  values ('khai_giang', 'bien', '15.10.2026', 'Ngay khai giang');
  perform pg_temp.dat('admin sua duoc noi dung trang');

  -- Loc the o luc GHI: du lieu sach tu trong kho, moi cho doc ve sau deu an toan ma
  -- khong phai nho loc lai.
  insert into eda_noi_dung (khoa, loai, gia_tri, mo_ta)
  values ('hero_tieu_de', 'bien', '<img src=x onerror=alert(1)>Xin chao', 'Tieu de');
  select gia_tri into v from eda_noi_dung where khoa = 'hero_tieu_de';
  if v like '%<%' or v like '%>%' then
    raise exception 'THAT BAI: the HTML khong bi loc, con "%"', v;
  end if;
  perform pg_temp.dat('the HTML bi loc ngay luc ghi: ' || v);

  select sua_boi::text into v from eda_noi_dung where khoa = 'khai_giang';
  if v is null then raise exception 'THAT BAI: khong ghi lai ai sua'; end if;
  perform pg_temp.dat('co ghi lai ai sua noi dung');
end $$;
commit;

begin;
set local role authenticated;
select pg_temp.dang_nhap('EDA_ACCOUNTANT', 'aaaaaaaa-0000-0000-0000-000000000002');
do $$
declare n integer;
begin
  select count(*) into n from eda_noi_dung;
  if n = 0 then raise exception 'THAT BAI: ke toan khong doc duoc noi dung trang'; end if;
  perform pg_temp.dat('ke toan DOC duoc noi dung trang');
end $$;
select pg_temp.phai_khong_doi(
  'ke toan KHONG sua duoc noi dung trang cong khai',
  $$update eda_noi_dung set gia_tri = '01.01.2000' where khoa = 'khai_giang'$$);
commit;

begin;
set local role authenticated;
select pg_temp.dang_nhap('EDA_TA', 'aaaaaaaa-0000-0000-0000-000000000003');
select pg_temp.phai_khong_doi(
  'tro giang KHONG sua duoc noi dung trang',
  $$update eda_noi_dung set gia_tri = '01.01.2000' where khoa = 'khai_giang'$$);
commit;

do $$
declare n integer;
begin
  select count(*) into n from eda_audit where bang = 'eda_noi_dung';
  if n < 2 then raise exception 'THAT BAI: doi noi dung trang cong khai khong duoc ghi nhat ky'; end if;
  perform pg_temp.dat(format('doi noi dung trang co vao nhat ky (%s dong)', n));
end $$;

-- ── Nhat ky khong sua duoc ─────────────────────────────────────────────────
begin;
set local role authenticated;
select pg_temp.dang_nhap('EDA_ADMIN', 'aaaaaaaa-0000-0000-0000-000000000001');
-- Ke ca admin. Mot nhat ky sua duoc thi khong con la bang chung, ma gia tri duy nhat
-- cua no la lam bang chung.
select pg_temp.phai_khong_doi('ADMIN cung khong xoa duoc nhat ky',
                         $$delete from eda_audit$$);
select pg_temp.phai_khong_doi('ADMIN cung khong sua duoc nhat ky',
                         $$update eda_audit set nguoi_dung = null$$);
commit;

\echo ''
\echo 'Tat ca kiem tra phan quyen deu dat.'

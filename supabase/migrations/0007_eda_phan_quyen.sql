-- Phan quyen 3 vai: EDA_TA (tro giang), EDA_ACCOUNTANT (ke toan), EDA_ADMIN.
--
-- Ranh gioi quan trong nhat: KE TOAN KHOP TIEN VAO, ADMIN QUYET DINH PHAI THU BAO NHIEU.
-- Neu mot tai khoan lam duoc ca hai thi mien giam khong roi khop cho khop so la thao tac
-- khong ai phat hien duoc. Day la tach nhiem vu, khong phai chuyen tien tay.
--
-- Vai doc tu app_metadata chu khong phai user_metadata: user_metadata do chinh nguoi dung
-- sua duoc luc dang ky, dat quyen o do la tu mo cua. Xem 0002.

create or replace function public.eda_vai()
returns text
language sql
stable
as $$ select auth.jwt() -> 'app_metadata' ->> 'role' $$;

create or replace function public.eda_la_admin()
returns boolean language sql stable as $$ select public.eda_vai() = 'EDA_ADMIN' $$;

create or replace function public.eda_dung_tien()
returns boolean language sql stable
as $$ select public.eda_vai() in ('EDA_ADMIN', 'EDA_ACCOUNTANT') $$;

-- ── Don dang ky ────────────────────────────────────────────────────────────
-- 0002 chi co mot vai EDA_ADMIN. Thay bang policy hieu ca ba vai.
drop policy if exists "eda admin read registration" on public.eda_registration;

create policy "doc don dang ky" on public.eda_registration
  for select to authenticated using (public.eda_dung_tien());

-- SUA THONG TIN CHI ADMIN. Ke toan doc duoc de doi chieu nhung khong sua duoc ho ten,
-- so dien thoai hay phuong an hoc phi cua ai.
create policy "sua don dang ky" on public.eda_registration
  for update to authenticated using (public.eda_la_admin()) with check (public.eda_la_admin());

-- Khong co policy INSERT/DELETE cho authenticated: don moi chi vao qua edge function
-- eda-register (service-role), va khong ai duoc xoa don tu trinh duyet.

-- ── Dot dong tien cua tung nguoi ───────────────────────────────────────────
create policy "doc dot dong" on public.eda_registration_installment
  for select to authenticated using (public.eda_dung_tien());

-- Mien giam, gia han, doi so tien phai dong deu la ADMIN. Day chinh la "phai thu bao
-- nhieu" - phan ke toan khong duoc dung toi.
create policy "sua dot dong" on public.eda_registration_installment
  for all to authenticated using (public.eda_la_admin()) with check (public.eda_la_admin());

-- Kiem VAI chu khong kiem "da dang nhap". Supabase mac dinh mo dang ky email, nen
-- auth.uid() is not null chi co nghia la "co ai do tu tao mot tai khoan", khong co nghia
-- la "nguoi cua minh". Ba vai duoi day phai do admin gan tay.
create policy "doc phuong an" on public.eda_payment_plan
  for select to authenticated using (public.eda_vai() is not null);
create policy "sua phuong an" on public.eda_payment_plan
  for all to authenticated using (public.eda_la_admin()) with check (public.eda_la_admin());

create policy "doc dot mau" on public.eda_plan_installment
  for select to authenticated using (public.eda_vai() is not null);
create policy "sua dot mau" on public.eda_plan_installment
  for all to authenticated using (public.eda_la_admin()) with check (public.eda_la_admin());

-- ── Sao ke va giao dich ────────────────────────────────────────────────────
create policy "doc lan upload" on public.eda_statement_upload
  for select to authenticated using (public.eda_dung_tien());
create policy "them lan upload" on public.eda_statement_upload
  for insert to authenticated with check (public.eda_dung_tien() and nguoi_upload = auth.uid());

create policy "doc giao dich" on public.eda_bank_txn
  for select to authenticated using (public.eda_dung_tien());
-- Rang buoc xac_nhan_boi phai co CA o duong INSERT, khong chi o UPDATE. Chi chan duong
-- update thi ke toan van chen thang mot dong da danh dau "da xac nhan boi <id admin>",
-- va nhat ky se ghi rang admin duyet khoan tien do.
create policy "them giao dich" on public.eda_bank_txn
  for insert to authenticated
  with check (public.eda_dung_tien()
              and (xac_nhan_luc is null or xac_nhan_boi = auth.uid()));

-- Ke toan sua duoc giao dich, nhung chi de KHOP va XAC NHAN.
-- Khong duoc tu xac nhan ho nguoi khac: xac_nhan_boi phai la chinh minh.
create policy "khop va xac nhan giao dich" on public.eda_bank_txn
  for update to authenticated
  using (public.eda_dung_tien())
  with check (public.eda_dung_tien()
              and (xac_nhan_luc is null or xac_nhan_boi = auth.uid()));

-- RLS chan duoc DONG nao sua, KHONG chan duoc COT nao sua. Neu chi dua vao policy tren
-- thi ke toan van co the sua so_tien hoac noi_dung cua mot giao dich - tuc la sua chinh
-- ban ghi sao ke de khop cho vua. Chan bang quyen o muc cot.
revoke update on public.eda_bank_txn from authenticated;
grant update (registration_id, installment_id, khop_kieu, xac_nhan_boi, xac_nhan_luc)
  on public.eda_bank_txn to authenticated;

-- Khong ai xoa giao dich tu trinh duyet: xoa mot dong sao ke la xoa dau vet tien vao.
-- Khop nham thi go khop (dat lai null), khong phai xoa.

-- ── Cong no: dat cong chan quyen ───────────────────────────────────────────
-- 0006 tao view nay khong co menh de where, vi luc do chua co eda_dung_tien(). View
-- khong bat security_invoker thi chay bang quyen chu so huu va BO QUA RLS cua ba bang
-- duoi, nen nguoi la cam anon key cong khai doc duoc het so phai dong / da dong cua tung
-- nguoi. Khong bat security_invoker duoc: tro giang khong co policy tren
-- eda_registration_installment va eda_bank_txn nen se mat sach du lieu. Vi vay cong duy
-- nhat la menh de where ngay trong view.
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
 -- Chi vai duoc dung tien. Khong dang nhap thi eda_vai() la null va loc het.
 where public.eda_dung_tien()
 group by r.id, distinct_i.can_thu;

-- ── Tro giang ──────────────────────────────────────────────────────────────
-- RLS chan theo DONG, khong chan theo COT, nen phan nay phai lam bang view rieng.
--
-- Ban dau cho view chay security_invoker = true roi them mot policy SELECT cho vai TA de
-- view di qua duoc RLS. Cach do SAI, va sai im lang:
--
--   RLS gan vao BANG chu khong gan vao duong truy cap. Postgres lai gop cac policy
--   permissive bang OR. Nen them "tro giang doc don" cho bang eda_registration khong chi
--   mo duong cho view, ma mo luon ca bang goc: tro giang goi thang
--   GET /rest/v1/eda_registration?select=guardian_phone la lay duoc so dien thoai phu
--   huynh - dung thu ma bang phan quyen tren giao dien ghi la CAM.
--
-- Nen bo han policy do. Tro giang khong cham vao bang goc nua, chi doc qua view. Doi lai,
-- view phai TU kiem vai trong menh de where, vi security_invoker = false thi view chay
-- bang quyen nguoi tao va bo qua RLS cua bang duoi.
create or replace view public.eda_registration_tro_giang
with (security_invoker = false) as
select r.id, r.code, r.name, r.phone, r.email, r.province, r.job, r.field, r.interest,
       r.facebook, r.zalo, r.channel, r.note, r.trang_thai, r.created_at,
       -- Du de biet ai duoc vao lop, khong lo ra so tien. Tinh thang tu bang goc chu
       -- KHONG qua view eda_cong_no: view do da chan lai cho vai dung tien, di qua no thi
       -- tro giang chi nhan duoc null.
       (coalesce(t.da_thu, 0) >= coalesce(i.can_thu, 0)) as da_dong_du
  from public.eda_registration r
  left join lateral (
    select sum(x.so_tien - x.mien_giam) as can_thu
      from public.eda_registration_installment x where x.registration_id = r.id
  ) i on true
  left join lateral (
    select sum(b.so_tien) as da_thu
      from public.eda_bank_txn b
      join public.eda_registration_installment x2 on x2.id = b.installment_id
     where x2.registration_id = r.id and b.xac_nhan_luc is not null
  ) t on true
 -- Cong duy nhat cua view: khong dang nhap thi eda_vai() la null va loc het.
 where public.eda_vai() in ('EDA_TA', 'EDA_ACCOUNTANT', 'EDA_ADMIN');
 -- KHONG co guardian_name, guardian_phone, khong co so tien.

drop policy if exists "tro giang doc don" on public.eda_registration;

grant select on public.eda_registration_tro_giang to authenticated;
grant select on public.eda_cong_no to authenticated;

-- ── Doc nhat ky ────────────────────────────────────────────────────────────
-- 0006 bat RLS tren eda_audit nhung khong dat policy SELECT nao, nghia la KHONG AI doc
-- duoc - ke ca admin. Mot nhat ky khong doc duoc thi khong lam duoc viec cua no.
--
-- Chi admin: moi dong chua ban chup truoc/sau cua ban ghi duoi dang jsonb, tuc la chua
-- ca SDT phu huynh va so tien. Cho ke toan hay tro giang doc nhat ky la di duong vong
-- qua dung cac cot ma ho bi cam xem.
create policy "doc nhat ky" on public.eda_audit
  for select to authenticated using (public.eda_la_admin());
grant select on public.eda_audit to authenticated;

-- ── Gan vai cho tai khoan ──────────────────────────────────────────────────
-- Chay trong SQL editor cua Supabase sau khi da tao user o muc Authentication.
-- Nguoi do phai dang xuat rong dang nhap lai thi JWT moi mang claim moi.
--
--   update auth.users
--      set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb)
--                              || '{"role":"EDA_ACCOUNTANT"}'::jsonb
--    where email = 'ke-toan@aivietnam.edu.vn';
--
-- Vai hop le: EDA_TA | EDA_ACCOUNTANT | EDA_ADMIN

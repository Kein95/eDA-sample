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

create policy "doc phuong an" on public.eda_payment_plan
  for select to authenticated using (auth.uid() is not null);
create policy "sua phuong an" on public.eda_payment_plan
  for all to authenticated using (public.eda_la_admin()) with check (public.eda_la_admin());

create policy "doc dot mau" on public.eda_plan_installment
  for select to authenticated using (auth.uid() is not null);
create policy "sua dot mau" on public.eda_plan_installment
  for all to authenticated using (public.eda_la_admin()) with check (public.eda_la_admin());

-- ── Sao ke va giao dich ────────────────────────────────────────────────────
create policy "doc lan upload" on public.eda_statement_upload
  for select to authenticated using (public.eda_dung_tien());
create policy "them lan upload" on public.eda_statement_upload
  for insert to authenticated with check (public.eda_dung_tien() and nguoi_upload = auth.uid());

create policy "doc giao dich" on public.eda_bank_txn
  for select to authenticated using (public.eda_dung_tien());
create policy "them giao dich" on public.eda_bank_txn
  for insert to authenticated with check (public.eda_dung_tien());

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

-- ── Tro giang ──────────────────────────────────────────────────────────────
-- RLS chan theo dong, khong chan theo cot, nen phan nay phai lam bang view rieng.
create or replace view public.eda_registration_tro_giang
with (security_invoker = true) as
select r.id, r.code, r.name, r.phone, r.email, r.province, r.job, r.field, r.interest,
       r.facebook, r.zalo, r.channel, r.note, r.trang_thai, r.created_at,
       -- Du de biet ai duoc vao lop, khong lo ra so tien.
       (n.da_dong >= n.phai_dong) as da_dong_du
  from public.eda_registration r
  left join public.eda_cong_no n on n.registration_id = r.id;
  -- KHONG co guardian_name, guardian_phone, khong co so tien.

create policy "tro giang doc don" on public.eda_registration
  for select to authenticated using (public.eda_vai() = 'EDA_TA');

-- security_invoker = true la BAT BUOC o day. Mac dinh view chay bang quyen nguoi tao
-- (thuong la postgres), nghia la RLS cua bang duoi bi bo qua va bat ky ai dang nhap cung
-- doc duoc. Voi security_invoker, view chay bang quyen nguoi goi nen policy tren van ap.

grant select on public.eda_registration_tro_giang to authenticated;
grant select on public.eda_cong_no to authenticated;

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

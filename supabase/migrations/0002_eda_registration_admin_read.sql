-- Cho phep tai khoan admin doc bang dang ky.
--
-- Migration 0001 bat RLS ma khong cap policy nao, nen ngoai service-role thi
-- khong ai doc duoc. Trang admin lai dang nhap bang tai khoan that (role
-- "authenticated"), nen can dung mot policy hep: chi tai khoan duoc gan
-- app_metadata.role = 'EDA_ADMIN' moi doc duoc.
--
-- Vi sao kiem tra app_metadata chu khong phai user_metadata: user_metadata do
-- chinh nguoi dung sua duoc khi dang ky, nen dat quyen o do la tu mo cua.
-- app_metadata chi service-role moi ghi duoc.
--
-- Gan quyen cho mot tai khoan (chay trong SQL editor cua Supabase, hoac qua
-- Admin API), sau khi da tao user do o muc Authentication:
--
--   update auth.users
--      set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb)
--                              || '{"role":"EDA_ADMIN"}'::jsonb
--    where email = 'nguoi-phu-trach@aivietnam.edu.vn';
--
-- Nguoi do phai dang xuat rong dang nhap lai thi JWT moi mang claim moi.

drop policy if exists "eda admin read registration" on public.eda_registration;
create policy "eda admin read registration" on public.eda_registration
  for select to authenticated
  using ((auth.jwt() -> 'app_metadata' ->> 'role') = 'EDA_ADMIN');

-- Khong cap insert/update/delete cho authenticated: ghi chi di qua edge function
-- eda-register (service-role), va khong ai duoc sua/xoa don dang ky tu trinh duyet.

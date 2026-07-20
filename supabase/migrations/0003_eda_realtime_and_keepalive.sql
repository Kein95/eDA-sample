-- 1) Realtime cho trang admin: don dang ky moi tu nhay vao bang, khong phai F5.
--
-- Realtime van di qua RLS, nen policy "eda admin read registration" o 0002 cung
-- la thu chan o day: tai khoan khong co role EDA_ADMIN se khong nhan duoc su kien.
alter publication supabase_realtime add table public.eda_registration;

-- REPLICA IDENTITY mac dinh chi gui khoa chinh trong payload cua UPDATE/DELETE.
-- Trang admin chi lang nghe INSERT nen mac dinh la du; dat FULL o day se lam
-- moi thay doi ghi them ban ghi cu vao WAL. Co tinh KHONG dat FULL.

-- 2) Chong Supabase free tier tu ngu dong sau 7 ngay khong co truy van.
--
-- Trang tuyen sinh co the im hang tuan giua hai dot quang ba, va neu du an ngu
-- thi don dang ky dau tien sau do se that bai. Mot truy van re moi ngay la du
-- de giu thuc. Bai hoc lay tu VNCLO, du an do da phai lam dung viec nay.
-- Tren Supabase: tao extension nhu binh thuong.
-- Tren Postgres thuan (docker/docker-compose.yml, de chay thu migration): khong co
-- extension nay. supabase/local/00-auth-gia.sql tao san schema "cron" gia, va dieu kien
-- duoi day nhan ra dieu do roi bo qua. Khong dung "exception when others" o day: nuot
-- moi loi thi mot ngay nao do pg_cron hong that ma migration van bao thanh cong.
do $$ begin
  if not exists (select 1 from pg_namespace where nspname = 'cron') then
    create extension if not exists pg_cron;
  end if;
end $$;

-- Bang dau chan, giu vai dong gan nhat de con biet cron co that su chay khong.
create table if not exists public.eda_keepalive (
  id         smallint primary key default 1,
  pinged_at  timestamptz not null default now(),
  constraint eda_keepalive_one_row check (id = 1)
);
alter table public.eda_keepalive enable row level security;   -- khong policy: khong ai doc tu trinh duyet

insert into public.eda_keepalive (id) values (1) on conflict (id) do nothing;

-- Go job cu truoc khi tao lai, de chay lai migration khong sinh job trung.
-- (Kiem tra cron.job truoc khi them job moi o bat ky du an Supabase nao.)
select cron.unschedule('eda-keepalive')
 where exists (select 1 from cron.job where jobname = 'eda-keepalive');

select cron.schedule(
  'eda-keepalive',
  '17 3 * * *',            -- 03:17 UTC moi ngay, tranh gio cao diem
  $$update public.eda_keepalive set pinged_at = now() where id = 1$$
);

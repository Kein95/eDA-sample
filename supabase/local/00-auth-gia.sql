-- Phan Supabase ma schema eDA thuc su phu thuoc, dung lai bang Postgres thuan.
--
-- Muc dich: chay THAT cac migration 0001-0007 tren postgres:16 thuan de kiem chung
-- rang buoc, trigger va RLS truoc khi tin la chung dung - va de tra loi cau hoi
-- "Postgres thi can gi Supabase". Toan bo phu thuoc Supabase cua schema nay nam gon
-- trong file duoi day: BA vai, MOT bang, HAI ham. Ngoai ra la Postgres thuan.
--
-- Tren Supabase that KHONG chay file nay: nhung thu nay da co san.
-- Chay:  psql -f supabase/local/00-auth-gia.sql

-- 1) Ba vai Supabase tao san. Migration co grant/revoke toi ca ba.
do $$ begin create role anon nologin;          exception when duplicate_object then null; end $$;
do $$ begin create role authenticated nologin; exception when duplicate_object then null; end $$;
do $$ begin create role service_role nologin;  exception when duplicate_object then null; end $$;

create schema if not exists auth;

-- 2) Bang nguoi dung. Cac bang tien co khoa ngoai tro toi day (ai xac nhan, ai upload).
create table if not exists auth.users (
  id    uuid primary key default gen_random_uuid(),
  email text unique
);

-- 3) Hai ham doc claim tu JWT.
--
-- Ban that cua Supabase doc bien phien "request.jwt.claims" do PostgREST dat truoc moi
-- truy van. Chep dung cach do de test co the gia lap mot nguoi dang nhap bang:
--   set local request.jwt.claims = '{"sub":"...","app_metadata":{"role":"EDA_ADMIN"}}';
create or replace function auth.jwt()
returns jsonb
language sql
stable
as $$
  select coalesce(nullif(current_setting('request.jwt.claim',  true), ''),
                  nullif(current_setting('request.jwt.claims', true), ''))::jsonb
$$;

create or replace function auth.uid()
returns uuid
language sql
stable
as $$
  select coalesce(
    nullif(current_setting('request.jwt.claim.sub', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')
  )::uuid
$$;

grant usage on schema auth to anon, authenticated, service_role;
grant select on auth.users to authenticated, service_role;

-- 3b) pg_cron gia. Postgres thuan khong co extension nay; migration 0003/0004 dung no
--     de giu du an khoi ngu va de xoa du lieu qua han. Tao san schema "cron" o day thi
--     0003 se BO QUA buoc create extension (xem chu thich trong 0003) va cac lenh
--     cron.schedule ben duoi van chay duoc, chi la khong co gi chay dinh ky - dung y,
--     day la CSDL dung thu.
create schema if not exists cron;

create table if not exists cron.job (
  jobid    bigserial primary key,
  jobname  text unique,
  schedule text,
  command  text
);

create or replace function cron.schedule(p_ten text, p_lich text, p_lenh text)
returns bigint language sql as $$
  insert into cron.job (jobname, schedule, command) values (p_ten, p_lich, p_lenh)
  on conflict (jobname) do update set schedule = excluded.schedule, command = excluded.command
  returning jobid
$$;

create or replace function cron.unschedule(p_ten text)
returns boolean language sql as $$
  delete from cron.job where jobname = p_ten returning true
$$;

-- 3c) Publication cho Realtime. Postgres thuan tao duoc publication binh thuong, chi la
--     khong co ai lang nghe. Du de 0003 chay qua.
do $$ begin
  create publication supabase_realtime;
exception when duplicate_object then null; end $$;

-- 4) Supabase mac dinh cap quyen bang trong schema public cho anon/authenticated roi
--    dung RLS lam cua. Migration 0007 REVOKE bot di tu diem xuat phat do, nen phai
--    tai dung diem xuat phat day thi moi kiem duoc that.
grant usage on schema public to anon, authenticated, service_role;
alter default privileges in schema public
  grant all on tables to anon, authenticated, service_role;
alter default privileges in schema public
  grant all on functions to anon, authenticated, service_role;
alter default privileges in schema public
  grant all on sequences to anon, authenticated, service_role;

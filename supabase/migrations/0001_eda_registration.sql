-- eDA 2026 enrolment capture.
--
-- Deliberately has NO unique constraint on email or phone: the landing page
-- supports registering on someone else's behalf, and a parent may legitimately
-- register two children from one email/phone. Duplicates are resolved by a
-- human at review time, not rejected at write time.

create table if not exists public.eda_registration (
  id             uuid primary key default gen_random_uuid(),
  code           text not null,               -- eDA26-XXXX shown back to the applicant
  name           text not null,
  phone          text not null,
  email          text not null,
  province       text,
  job            text,                        -- "Sinh viên" / "Học sinh" / "Đi làm" ...
  field          text,                        -- current major or occupation
  interest       text,                        -- "Ứng dụng" / "Chuyên sâu" ...
  guardian_name  text,                        -- minors only
  guardian_phone text,                        -- minors only
  -- Kenh lien he phu: nhieu nguoi dung Zalo bang so khac so dang ky, va tu van
  -- vien thuong chot qua Facebook. Ca hai deu tuy chon.
  facebook       text,
  zalo           text,
  channel        text,                        -- how they heard about eDA 2026
  note           text,
  user_agent     text,
  created_at     timestamptz not null default now()
);

create index if not exists eda_registration_created_idx on public.eda_registration (created_at desc);
-- Supports the manual duplicate review described above.
create index if not exists eda_registration_phone_idx on public.eda_registration (phone);
create index if not exists eda_registration_email_idx on public.eda_registration (lower(email));

-- This table holds contact details of minors and their guardians.
-- RLS is enabled with NO policies on purpose: anon and authenticated roles get
-- nothing at all. Only the service-role key (which bypasses RLS, and is used
-- solely by the eda-register edge function) can write, and reading is done
-- through the Supabase dashboard by a project member. Do not add a permissive
-- policy here without deciding who is allowed to read guardian data.
alter table public.eda_registration enable row level security;

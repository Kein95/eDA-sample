-- 1) Cot phuc vu gioi han tan suat theo IP.
--
-- Luu BAM cua IP chu khong luu IP tho: de dem "cung mot nguoi gui bao nhieu don trong
-- mot gio" thi chi can biet trung hay khong trung, khong can biet IP that. Bam kem
-- EDA_IP_SALT nen ke co bang cung khong dao nguoc ra IP duoc.
alter table public.eda_registration add column if not exists ip_hash text;

-- Truy van gioi han tan suat luon la (ip_hash, created_at) trong 1 gio gan nhat.
create index if not exists eda_registration_ip_hash_idx
  on public.eda_registration (ip_hash, created_at desc)
  where ip_hash is not null;

-- 2) Xoa du lieu qua han.
--
-- Bang nay giu ho ten, so dien thoai, email cua hoc vien VA ten + so dien thoai
-- nguoi giam ho cua tre vi thanh nien. Giu vo thoi han la rui ro khong can thiet:
-- du lieu con nam do ngay nao thi con co the ro ri ngay do. Khoa khai giang 09.2026
-- va ket thuc 05.2027, nen 24 thang la du rong cho tuyen sinh, cham soc va doi soat.
--
-- CO Y de mac dinh 24 thang thay vi ngan hon: xoa nham don dang ky cua nguoi that
-- gay thiet hai lon hon la giu them vai thang.
create or replace function public.eda_xoa_dang_ky_qua_han()
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare n integer;
begin
  delete from public.eda_registration
   where created_at < now() - interval '24 months';
  get diagnostics n = row_count;
  return n;
end;
$$;

revoke all on function public.eda_xoa_dang_ky_qua_han() from public, anon, authenticated;

-- Chay hang thang. Go job cu truoc de chay lai migration khong sinh job trung.
select cron.unschedule('eda-xoa-qua-han')
 where exists (select 1 from cron.job where jobname = 'eda-xoa-qua-han');

select cron.schedule(
  'eda-xoa-qua-han',
  '41 4 1 * *',                -- 04:41 UTC ngay 1 hang thang
  $$select public.eda_xoa_dang_ky_qua_han()$$
);

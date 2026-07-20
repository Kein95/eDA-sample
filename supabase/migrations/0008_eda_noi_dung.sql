-- Noi dung trang sua duoc tu trang quan tri, khong phai sua code.
--
-- Pham vi CO Y hep: chi sua CHU VA SO co san, khong them/bot/doi thu tu khoi. Trang
-- tuyen sinh la mot thiet ke da can tay ky (chip 8 module, dai ngang, qua dia cau,
-- timeline chevron); cho them khoi tuy y dong nghia voi viec moi thay doi noi dung deu
-- co the pha bo cuc, va se can mot trinh dung trang that su - do la san pham khac.

-- Hai loai noi dung, hai co che thay khac nhau:
--   'bien' - chuoi lap GIUA cau van, khoa la ten dat san (khai_giang, gio_hoc...) va
--            khop voi the <script id="noi-dung-mac-dinh"> tren trang. Ngay khai giang
--            hien o 12 cho, moi cho mot cau khac nhau nen phai thay theo chuoi con.
--   'chu'  - moi chu con lai. Khoa la CHINH CHUOI GOC, va trang khop CA node van ban
--            chu khong khop mot phan: trang co hon 600 chuoi, trong do co "8", "AI",
--            "·" - thay theo chuoi con voi nhung chuoi nay se sua nham khap trang.
create table if not exists public.eda_noi_dung (
  khoa       text primary key,               -- 'bien': ten khoa | 'chu': chinh chuoi goc
  loai       text not null default 'chu' check (loai in ('bien', 'chu')),
  gia_tri    text not null,
  mo_ta      text not null default '',       -- hien cho nguoi sua biet day la cho nao
  da_xuat_ban boolean not null default false,
  sua_boi    uuid references auth.users(id),
  sua_luc    timestamptz not null default now()
);

-- Gia tri MAC DINH khong nam trong bang nay. No nam trong chinh markup cua trang
-- (the <script id="noi-dung-mac-dinh">), vi mot ly do: trang phai hien du chu ngay ca
-- khi CSDL ngu, hong, hay chua co ban ghi nao. Bang nay chi chua phan CHONG LEN.
-- Mot trang tuyen sinh trang chu vi may chu khong phan hoi thi hong nang hon la hien
-- noi dung cu vai phut.

-- Loc the o luc GHI chu khong phai luc doc.
--
-- Nguoi sua noi dung khong duoc phep chen the vao trang cong khai. Day la XSS do nguoi
-- trong nha gay ra, van la XSS. Loc luc ghi thi du lieu sach tu trong kho, moi cho doc
-- ve sau deu an toan ma khong phai nho loc lai.
create or replace function public.eda_loc_the_noi_dung()
returns trigger
language plpgsql
as $$
begin
  new.gia_tri := replace(replace(new.gia_tri, '<', ''), '>', '');
  new.sua_luc := now();
  new.sua_boi := auth.uid();
  return new;
end;
$$;

drop trigger if exists eda_loc_the_noi_dung_trg on public.eda_noi_dung;
create trigger eda_loc_the_noi_dung_trg
  before insert or update on public.eda_noi_dung
  for each row execute function public.eda_loc_the_noi_dung();

-- Nhat ky: dung chung ham voi cac bang tien. Doi noi dung trang cong khai la thao tac
-- co hau qua doi ngoai, phai biet ai doi va doi thanh gi.
drop trigger if exists eda_log_trg on public.eda_noi_dung;
create trigger eda_log_trg
  after insert or update or delete on public.eda_noi_dung
  for each row execute function public.eda_ghi_log();

alter table public.eda_noi_dung enable row level security;

-- Doc: moi tai khoan CO VAI (tro giang cung can xem trang dang noi gi).
-- Ghi: chi admin. Ke toan khong sua noi dung trang cong khai, tro giang cung khong.
--
-- Kiem vai chu khong kiem "da dang nhap": Supabase mac dinh mo dang ky email, nen
-- auth.uid() is not null chi co nghia la co ai do tu tao mot tai khoan.
create policy "doc noi dung" on public.eda_noi_dung
  for select to authenticated using (public.eda_vai() is not null);
create policy "sua noi dung" on public.eda_noi_dung
  for all to authenticated using (public.eda_la_admin()) with check (public.eda_la_admin());

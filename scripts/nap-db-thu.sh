#!/usr/bin/env bash
# Dung lai CSDL thu tu dau roi nap toan bo migration.
#
#   bash scripts/nap-db-thu.sh
#
# Dung Postgres THUAN (postgres:16-alpine), khong phai anh Supabase - de biet schema
# nay thuc su can bao nhieu phan Supabase. Phan can duoc dung lai trong
# supabase/local/00-auth-gia.sql.
#
# Truyen SQL qua stdin chu khong dua duong dan cho psql: Git Bash tren Windows tu doi
# "/tmp/x.sql" thanh "C:/Users/.../tmp/x.sql" truoc khi container nhin thay.
set -euo pipefail

CT=eda-db
DB=eda
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

chay() {   # chay <duong-dan-sql>
  local f="$1"
  printf '  %-46s' "$(basename "$f")"
  # ON_ERROR_STOP=1 de mot lenh hong la dung han, khong chay tiep tren nen da hong.
  if out=$(docker exec -i "$CT" psql -U postgres -d "$DB" -v ON_ERROR_STOP=1 -q < "$f" 2>&1); then
    echo "OK"
  else
    echo "HONG"
    echo "$out" | sed 's/^/      /'
    return 1
  fi
}

echo "1) Xoa va tao lai schema public"
docker exec -i "$CT" psql -U postgres -d "$DB" -v ON_ERROR_STOP=1 -q <<'SQL'
drop schema if exists public cascade;
drop schema if exists auth cascade;
drop schema if exists cron cascade;
drop publication if exists supabase_realtime;
create schema public;
SQL

echo "2) Dung lai phan Supabase (auth, cron, publication)"
chay "$GOC/supabase/local/00-auth-gia.sql"

echo "3) Nap migration"
for f in "$GOC"/supabase/migrations/*.sql; do chay "$f"; done

echo
echo "Bang da tao:"
docker exec -i "$CT" psql -U postgres -d "$DB" -tAc \
  "select '  '||tablename from pg_tables where schemaname='public' order by 1"

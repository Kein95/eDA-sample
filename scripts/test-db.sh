#!/usr/bin/env bash
# Dung lai CSDL, nap migration, roi chay toan bo kiem tra schema va phan quyen.
#
#   bash scripts/test-db.sh
#
# Can Docker chay va container eda-db:
#   docker compose -f docker/docker-compose.yml up -d eda-db
set -euo pipefail

CT=eda-db
DB=eda
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! docker ps --format '{{.Names}}' | grep -qx "$CT"; then
  echo "Chua co container $CT. Chay truoc:"
  echo "  docker compose -f docker/docker-compose.yml up -d eda-db"
  exit 1
fi

bash "$GOC/scripts/nap-db-thu.sh" > /dev/null

chay() {
  echo "== $(basename "$1")"
  # grep -v de bo tien to "NOTICE:" cho de doc; ON_ERROR_STOP=1 lo hong la thoat khac 0.
  docker exec -i "$CT" psql -U postgres -d "$DB" -v ON_ERROR_STOP=1 -q < "$1" 2>&1 \
    | sed 's/^NOTICE:  //' | grep -v '^$'
}

chay "$GOC/supabase/local/test-schema.sql"
echo
chay "$GOC/supabase/local/test-phan-quyen.sql"

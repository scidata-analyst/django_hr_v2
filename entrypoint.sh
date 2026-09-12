#!/bin/sh
# HRMSPro web entrypoint.
#
# Guarantees the database schema exists BEFORE the server accepts requests,
# so the app can never serve traffic against an unmigrated database
# (which surfaces as: ProgrammingError 1146 "Table 'django_db.auth_user'
# doesn't exist").
#
# Steps:
#   1. Run `migrate --noinput`, retrying while MySQL is still coming up.
#      If migrations ultimately fail, the container exits non-zero and the
#      server is NOT started (fail fast instead of serving 500s).
#   2. Run the demo `seed` (idempotent via --if-empty; never fatal).
#   3. Exec the CMD passed by Docker (e.g. runserver).
#
# Tunables (environment):
#   MIGRATE_RETRIES     - max migrate attempts (default 12)
#   MIGRATE_RETRY_DELAY - seconds between attempts (default 5)
set -e

MIGRATE_RETRIES="${MIGRATE_RETRIES:-12}"
MIGRATE_RETRY_DELAY="${MIGRATE_RETRY_DELAY:-5}"

attempt=1
until python root/manage.py migrate --noinput; do
  if [ "$attempt" -ge "$MIGRATE_RETRIES" ]; then
    echo "ERROR: 'manage.py migrate' failed after $attempt attempt(s) - refusing to start the server." >&2
    echo "HINT: check that the database is reachable (DB_HOST/DB_PORT/DB_USER/DB_PASSWORD) and its logs." >&2
    exit 1
  fi
  echo "migrate failed (attempt $attempt/$MIGRATE_RETRIES) - retrying in ${MIGRATE_RETRY_DELAY}s..."
  attempt=$((attempt + 1))
  sleep "$MIGRATE_RETRY_DELAY"
done

# `migrate` already auto-seeds an empty DB via the post_migrate signal;
# this explicit call is a harmless fallback (--if-empty skips when seeded).
python root/manage.py seed --if-empty --full || echo "WARNING: demo seeding skipped/failed - starting server anyway."

exec "$@"

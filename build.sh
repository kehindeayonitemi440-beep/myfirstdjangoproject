#!/usr/bin/env bash
# Render build script: runs on every deploy.
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Creates the admin login once, from env vars. Never overwrites an existing user.
python manage.py ensure_superuser

# Loads the sample fabrics/reviews on first deploy. Turn off afterwards
# (set SEED_SAMPLE_DATA=0) so deleted samples don't come back.
if [ "${SEED_SAMPLE_DATA:-0}" = "1" ]; then
  python manage.py seed_shop
fi

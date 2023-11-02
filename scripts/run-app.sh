#!/bin/bash
set -ex

python3 manage.py collectstatic --noinput

exec python3 app.py --no-debug $@

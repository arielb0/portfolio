#!/usr/bin/env bash
# exit on error
set -o errexit
pip3 install -r requirements.txt
./manage.py collectstatic --no-input
./manage.py migrate
./manage.py loaddata bazaar/permissions bazaar/groups restaurant/answers
#!/usr/bin/env bash

source /var/www/app/portfolio/venv/bin/activate
/var/www/app/portfolio/manage.py delete_old_ads

exit

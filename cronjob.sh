#!/usr/bin/env bash

source /var/www/app/venv/bin/activate

/var/www/app/portfolio/manage.py bazaar_delete_old_ads
/var/www/app/porfolio/manage.py accounts_delete_inactive_users
/var/www/app/portfolio/manage.py accounts_notify_inactive_users

exit
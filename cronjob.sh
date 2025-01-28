#!/usr/bin/env bash

source /var/www/app/venv/bin/activate
/var/www/app/portfolio/manage.py bazaar_delete_old_ads
# Execute more scheduled tasks here..

exit
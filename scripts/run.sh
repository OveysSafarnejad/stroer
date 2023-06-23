#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

USER="admin"
PASS="admin"
MAIL="admin@mail.com"
script="
from django.contrib.auth import get_user_model;
User = get_user_model();

username = '$USER';
password = '$PASS';
email = '$MAIL';

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
# shellcheck disable=SC2059
printf "$script" | python manage.py shell

python manage.py fetch_posts
python manage.py fetch_comments


uwsgi --socket :${APP_PORT} --workers 4 --master --enable-threads --module stroer.wsgi
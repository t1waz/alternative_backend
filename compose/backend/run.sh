#bin/bash

#uwsgi /manage/app_uwsgi.ini
python /app/manage.py runserver 0.0.0.0:8000

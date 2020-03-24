#bin/bash

docker-compose -f docker-compose-dev.yml run django-app python /app/manage.py loaddata /manage/seed_db.json
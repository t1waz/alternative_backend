#bin/bash

docker-compose -f docker-compose-dev.yml run django-app python /app/manage.py loaddata /app/seed_db.json
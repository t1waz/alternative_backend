#bin/bash

sudo docker-compose run django-app python /app/manage.py loaddata /app/seed_db.json
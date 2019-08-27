#bin/bash

sudo docker-compose exec web python manage.py loaddata seed_db.json
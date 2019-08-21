#bin/bash

sudo docker-compose run web python manage.py loaddata seed_db.json

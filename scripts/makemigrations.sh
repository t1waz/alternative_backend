#bin/bash

sudo docker-compose run web python manage.py makemigrations
sudo docker-compose run web python manage.py migrate
sudo docker-compose run web python manage.py collectstatic --pythonpath / --no-input

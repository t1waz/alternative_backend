#bin/bash

docker-compose -f docker-compose-dev.yml run django-app python manage.py shell

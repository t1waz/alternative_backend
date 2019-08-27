#bin/bash

python manage.py migrate
python manage.py collectstatic --pythonpath / --no-input
#python manage.py loaddata seed_db.json
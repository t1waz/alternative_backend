#bin/bash

python /app/manage.py migrate
python /app/manage.py collectstatic --pythonpath / --no-input
#python manage.py loaddata seed_db.json
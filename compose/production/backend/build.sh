#bin/bash

python manage.py migrate
python manage.py collectstatic --pythonpath / --no-input
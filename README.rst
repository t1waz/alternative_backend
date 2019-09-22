ALTERNATIVE BACKEND
===================

App purpose's to serve backend service for Alternative Longboards company.

How to setup
------------

Run command from docker-compose.yml dir:
	$ chmod +x scripts/setup_project.sh

Setup project:
	$ .scripts/setup_project.sh

Usage
-----

Build dockers (use in pip packages changes, or deploy itself):
	$ ./scripts/build.sh

Load fixtures from alternative_backend/seed_db.json:
	$ ./scripts/load_fixtures.sh

Easy make migrations:
	$ ./scripts/makemigrations.sh

Run containers and project in develop stage:
	$ ./scripts/start_dev.sh

Run containers and project in production stage:
	$ ./scripts/start_prod.sh

Stop containers and project:
	$ ./scripts/stop.sh

Run tests:
	$ ./scripts/tests.sh

Check style with flake8:
	$ ./scripts/check_style.sh

Enjoy !
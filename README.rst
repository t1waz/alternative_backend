ALTERNATIVE BACKEND
===================

App purpose's to serve backend service for Alternative Longboards company.

How to setup
------------

Run commands from docker-compose.yml dir:
	$ chmod +x scripts/build.sh

	$ chmod +x scripts/load_fixtures.sh

	$ chmod +x scripts/makemigrations.sh

	$ chmod +x scripts/runserver.sh

	$ chmod +x scripts/stopserver.sh

	$ chmod +x scripts/tests.sh

Setup project:
	$ .scripts/makemigrations.sh

	$ .scripts/load_fixtures.sh

Usage
-----

Build dockers (use in pip packages changes, or deploy itself):
	$ ./scripts/build.sh

Load fixtures from alternative_backend/seed_db.json:
	$ ./scripts/load_fixtures.sh

Easy make migrations:
	$ ./scripts/makemigrations.sh

Run containers and project in develop stage:
	$ ./scripts/runserver.sh

Stop containers and project in develop stage:
	$ ./scripts/stopserver.sh

Run tests:
	$ ./scripts/tests.sh

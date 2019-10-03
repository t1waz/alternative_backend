ALTERNATIVE BACKEND
===================

App purpose's to serve backend service for Alternative Longboards company.

How to setup
------------

Create .envs dir:
	$ mkdir .envs

	$ touch django.env

	$ touch postgres.env


Fill .envs with data:

	django.envs:

		DEVELOPMENT_ACCESS_TOKEN=<YOUR_KEY>

		PRODUCTION_ACCESS_TOKEN=<YOUR_KEY>

	postgres.envs:

		POSTGRES_DB=<YOUR_VALUE> (default: postgres)

		POSTGRES_USER=<YOUR_VALUE> (default: postgres)

		POSTGRES_PASSWORD=<YOUR_VALUE> (default: not_very_secret_password)

		POSTGRES_HOST=<YOUR_VALUE> (default: db)

		POSTGRES_PORT=<YOUR_VALUE> (default: 5432)


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
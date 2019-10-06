ALTERNATIVE BACKEND
===================

App purpose's to serve backend service for Alternative Longboards company.


How to setup
------------

Create .envs resources:

	$ mkdir .envs/development

	$ mkdir .envs/production

	$ touch .envs/development/django.env

	$ touch .envs/development/postgres.env

	$ touch .envs/production/django.env

	$ touch .envs/production/postgres.env


Fill .envs with data:

	django.envs:

		ACCESS_TOKEN=<YOUR_KEY>
		SETTINGS_PATH=settings.development or settings.production

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

Development build:

	$ ./scripts/dev_build.sh

Load fixtures from alternative_backend/seed_db.json:

	$ ./scripts/dev_load_fixtures.sh

Make migrations:

	$ ./scripts/dev_makemigrations.sh

Run development enviroment:

	$ ./scripts/dev_start.sh

Run production enviroment:

	$ ./scripts/prod_start.sh

Stop development enviorment:

	$ ./scripts/dev_stop.sh

Stop production enviorment:

	$ ./scripts/prod_stop.sh

Run tests:

	$ ./scripts/tests.sh

Check style with flake8:

	$ ./scripts/check_style.sh


Enjoy !
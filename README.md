ALTERNATIVE BACKEND
===================

App purpose's to serve backend service for Alternative Longboards company.


How to setup
------------

Run

	$ sudo echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf

	$ sudo sysctl vm.overcommit_memory=1

Edit /etc/default/grub to add transparent_hugepage=never to the GRUB_CMDLINE_LINUX_DEFAULT option:

	GRUB_CMDLINE_LINUX_DEFAULT="transparent_hugepage=never quiet splash"

Install docker-compose:

	apt-get install docker-compose

Run:

	$ sudo update-grub

Reboot system

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
ALTERNATIVE BACKEND
===================

App purpose's to serve backend service for Alternative Longboards company.

How to setup
------------

Install project venv:
	python3.6 -m venv .venv

Activate venv env:	
	source .venv/bin/activate

Install packages:
	pip install -r requirements.txt

Load fixtures:
	python manage.py loaddata utils/dump.json


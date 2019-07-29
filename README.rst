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

Deploy project:
    python manage.py makemigrations
    python manage.py migrate

Load fixtures:
	python manage.py loaddata seed_db.json

Run project:
	python manage.py runserver


DEPLOY
------

Create service
	$ sudo nano /etc/systemd/system/<app_name>.service

	[Unit]

	Description=gunicorn daemon for <app_name>
	After=network.target
	
	[Service]

	WorkingDirectory=<path_to_app_manage.py>
	ExecStart=<path_to_app_venv>/bin/gunicorn --workers 3 --bind unix:/tmp/<app_name>.sock <path_to_folder_with_app_wsgi>.wsgi:application

	[Install]

	WantedBy=multi-user.target

Run service
	sudo systemctl start <app_name>
	sudo systemctl daemon-reload
	sudo systemctl status <app_name>
	sudo systemctl enable <app_name>
	sudo systemctl status <app_name>

Create nginx config
	$ nano /etc/nginx/sites-available/<app_name>

	server {
	    listen <port>;
	    server_name 0.0.0.0;
	
	    location = /favicon.ico { access_log off; log_not_found off; }

	    location /static/ {
	            root <app_static_folder_best_to_store_in_tmp>;
	    }

	    location / {
	            proxy_set_header Host $http_host;
	            proxy_set_header X-Real-IP $remote_addr;
	            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	            proxy_set_header X-Forwarded-Proto $scheme;
	            include proxy_params;
            proxy_pass http://unix:/tmp/<app_name>.sock;
	    }
	}

	$ sudo ln -s /etc/nginx/sites-available/<app_name>  /etc/nginx/sites-enabled/
	$ sudo nginx -t
	$ sudo service nginx restart

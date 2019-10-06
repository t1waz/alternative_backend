FROM python:3

WORKDIR /app

RUN mkdir /manage

RUN mkdir /entrypoint

COPY ./alternative_backend /app

COPY ./requirements.txt /app

COPY ./compose/production/backend/run.sh /manage
RUN chmod +x /manage/run.sh

COPY ./compose/production/backend/build.sh /manage
RUN chmod +x /manage/build.sh

COPY ./compose/production/backend/entrypoint.sh /entrypoint
RUN chmod +x /entrypoint/entrypoint.sh

COPY ./compose/production/backend/app_uwsgi.ini /manage

RUN pip install --upgrade pip \
	&& pip install -r /app/requirements.txt

ENTRYPOINT ["/entrypoint/entrypoint.sh"]

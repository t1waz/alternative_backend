FROM python:3

WORKDIR /manage

RUN mkdir /app

RUN mkdir /entrypoint

COPY ./requirements.txt /app

COPY ./compose/backend/run.sh /manage
RUN chmod +x /manage/run.sh

COPY ./compose/backend/dev_run.sh /manage
RUN chmod +x /manage/dev_run.sh

COPY ./compose/backend/prod_run.sh /manage
RUN chmod +x /manage/prod_run.sh

COPY ./compose/backend/build.sh /manage
RUN chmod +x /manage/build.sh

COPY ./compose/backend/entrypoint.sh /entrypoint
RUN chmod +x /entrypoint/entrypoint.sh

COPY ./compose/backend/app_uwsgi.ini /manage

RUN pip install --upgrade pip \
	&& pip install -r /app/requirements.txt

ENTRYPOINT ["/entrypoint/entrypoint.sh"]
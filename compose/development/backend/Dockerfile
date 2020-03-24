FROM python:3

WORKDIR /app

RUN mkdir /manage

RUN mkdir /entrypoint

COPY ./requirements.txt /app

COPY ./seed_db.json /manage

COPY ./compose/development/backend/run.sh /manage
RUN chmod +x /manage/run.sh

COPY ./compose/development/backend/build.sh /manage
RUN chmod +x /manage/build.sh

COPY ./compose/development/backend/entrypoint.sh /entrypoint
RUN chmod +x /entrypoint/entrypoint.sh

RUN pip install --upgrade pip \
	&& pip install -r /app/requirements.txt

ENTRYPOINT ["/entrypoint/entrypoint.sh"]

FROM python:3

WORKDIR /app

RUN mkdir /manage

COPY ./requirements.txt /app

COPY ./compose/backend/run.sh /manage

COPY ./compose/backend/app_uwsgi.ini /manage

RUN pip install --upgrade pip \
	&& pip install -r requirements.txt

RUN chmod +x /manage/run.sh



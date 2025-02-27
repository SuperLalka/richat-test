FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
  # psycopg2 dependencies
  && apt-get install gcc -y \
  && apt-get install libpq-dev -y \
  # for Django translations
  && apt-get install gettext -y

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/base.txt

COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

WORKDIR /app

ENTRYPOINT ["/entrypoint"]

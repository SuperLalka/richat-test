FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1

RUN apt-get update -y \
  # psycopg2 dependencies
  && apt-get install gcc -y \
  && apt-get install libpq-dev -y \
  # for Django translations
  && apt-get install gettext -y \
  # for crontab
  && apt-get install cron -y

COPY ./requirements /requirements
RUN pip install -r /requirements/base.txt

COPY ./entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY . /app

WORKDIR /app

EXPOSE 80

ENTRYPOINT ["/entrypoint"]

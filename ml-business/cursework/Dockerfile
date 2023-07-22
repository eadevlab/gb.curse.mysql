FROM python:3.8.17

LABEL maintainer="no-mail@do_not.want_to"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN python ./app/build.py

EXPOSE 8080

VOLUME /app/models

COPY ./docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
FROM python:3.7

LABEL maintainer="no-mail@do_not.want_to"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN python ./models/build.py

EXPOSE 8180

VOLUME /app/models

COPY ./docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
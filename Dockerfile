FROM python:3.9

RUN curl -sSL https://install.python-poetry.org/ | python -
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
ENV PATH /root/.local/bin:$PATH
COPY landing /landing
WORKDIR landing
RUN poetry install

EXPOSE 8000

CMD poetry run gunicorn landing.wsgi:application --bind localhost:$PORT
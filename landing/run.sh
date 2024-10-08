#!/bin/bash
echo "source $(poetry env info --path)/bin/activate" >> /root/.bashrc
source $(poetry env info --path)/bin/activate

poetry run python manage.py migrate
poetry run python manage.py findstatic .
poetry run python manage.py collectstatic --noinput
if [ "$1" == "prod" ]; then
    poetry run poetry add gunicorn
    poetry run gunicorn landing.wsgi:application --bind 0.0.0.0:$PORT
else
    poetry run python manage.py runserver 0.0.0.0:$PORT
fi

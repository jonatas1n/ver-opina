#!/bin/bash
echo "source $(poetry env info --path)/bin/activate" >> /root/.bashrc
source $(poetry env info --path)/bin/activate

python manage.py migrate
python manage.py migrate
python manage.py findstatic .
python manage.py collectstatic --noinput
poetry install
poetry add gunicorn
gunicorn landing.wsgi:application --bind 0.0.0.0:$PORT

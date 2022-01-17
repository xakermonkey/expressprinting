#!/bin/bash

python manage.py makemigrations operator_part
python manage.py makemigrations user_part
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('operator', '', 'kjnw7fdk!d7fbko8y4')" | python manage.py shell
gunicorn --bind 0.0.0.0:8000 expressprinting.wsgi
#!/bin/sh

if [ "$ENV_TYPE" = "production" ]
then
  echo "Waiting for postgres..."

  while ! nc -z db 5432; do
    sleep 0.1
  done

  echo "PostgreSQL started"

  # python manage.py flush --no-input
  python manage.py collectstatic --noinput --settings=backend.settings.production
  python manage.py makemigrations --noinput --settings=backend.settings.production
  python manage.py migrate --noinput --settings=backend.settings.production

  exec "$@"
fi
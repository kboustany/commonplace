#!/bin/bash

echo "Runtime ENV: DEV=$DEV"

if [ "$DEV" = "false" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput

    echo "Running collectstatic..."
    python manage.py collectstatic --noinput

    echo "Starting Gunicorn..."
    exec gunicorn commonplace.wsgi:application --bind 0.0.0.0:8000
else
    echo "DEV mode detected, skipping migrate, collectstatic and gunicorn start."
    exit 0
fi
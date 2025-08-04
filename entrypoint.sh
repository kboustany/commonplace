#!/bin/bash

echo "Runtime ENV: DEV=$DEV"

if [ "$DEV" = "false" ]; then
    echo "Running collectstatic..."
    python manage.py collectstatic --noinput

    echo "Starting Gunicorn..."
    exec gunicorn commonplace.wsgi:application --bind 0.0.0.0:8000
else
    echo "DEV mode detected, skipping collectstatic and gunicorn start."
    # Optionally you can just exit or run some default command or sleep to keep container alive
    exit 0
fi
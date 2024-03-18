#!/usr/bin/env bash
# Exit on error -- this is for render
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)

cd ./backend && pipx install poetry && poetry install && poetry env use python3.12.2
echo 'I executed properly by my own Kalume'

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
# python manage.py migrate

# to control this you set environment variable in render control panel

if [[ "$CREATE_SUPERUSER" = "YES" ]] ; then
    python manage.py createsuperuser --no-input
fi


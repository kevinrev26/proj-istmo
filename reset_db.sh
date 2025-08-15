#!/usr/bin/env bash

# Stop on errors
set -e

echo "==== Cleaning project"
rm -f db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -r {} +

echo "==== Reinstalling Django"
pip uninstall django -y || true
pip install --force-reinstall django

echo "==== Rebuilding database"
python manage.py makemigrations
python manage.py migrate

echo "==== Creating superuser"
python manage.py createsuperuser

echo "==== Reset complete!"
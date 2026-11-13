#!/usr/bin/env bash
# Script de build utilisé par l'hébergeur (Render, Railway…) avant le démarrage.
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

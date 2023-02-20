#!/usr/bin/bash
cd backend/$1

source env/scripts/activate

python manage.py runserver 5010
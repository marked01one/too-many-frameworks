#!/usr/bin/bash

runserver() {
  cd backend/pythondjango
  source env/scripts/activate
  python manage.py runserver 5010
}

runserver

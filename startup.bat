:: script.bat

@echo off

start cmd /k "cd src\gui && npm run dev"

start cmd /k "cd src\code && python setup.py && python manage.py runserver"
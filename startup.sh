#!/bin/bash

# Script.sh

# Run React server
gnome-terminal --tab -- bash -c "cd src/gui && npm run dev; exec bash"

# Run Django server
gnome-terminal --tab -- bash -c "cd src/code && python setup.py && python manage.py runserver; exec bash"
#!/bin/bash

#assumes you are in a virtual env.

echo "Verifying requirements..."
python -m pip install -r requirements.txt

echo "Re-initializing database..."
python create_db.py

echo "Populating database..."
python twitter.py

echo "Starting webserver..."
python app.py

#!/bin/bash

cd backend || exit

alembic upgrade head

python start_app.py

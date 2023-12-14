#!/bin/bash

cd backend || exit

alembic uprade head

python start_app.py

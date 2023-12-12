#!/bin/bash

cd backend/app/api || exit

uvicorn main:app --host "0.0.0.0" --port "8000"

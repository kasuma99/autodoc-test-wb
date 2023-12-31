#!/bin/bash


REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_DB="${REDIS_DB:-0}"

cd backend || exit

celery -A app.tasks.celery_app:celery_app flower --broker="redis://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}" --port=5555

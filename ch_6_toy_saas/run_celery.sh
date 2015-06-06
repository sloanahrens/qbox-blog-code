#!/usr/bin/env bash

. venv/bin/activate
celery worker -A flaskapp.celery --loglevel=info --concurrency=1
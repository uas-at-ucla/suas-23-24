#!/bin/sh

gunicorn main:app -w 2 -b 0.0.0.0:8003 --access-logfile -

exec "$@"

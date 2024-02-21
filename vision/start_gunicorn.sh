#!/bin/sh

gunicorn main:app -w 1 -b 0.0.0.0:8003 --chdir ./vision -c ./vision/gunicorn.conf.py --access-logfile -
echo "server started"

exec "$@"

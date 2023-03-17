#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py create_db

# If additional command-line arguments are provided, execute them.
# Otherwise, run the Flask development server.
if [ $# -gt 0 ]; then
    exec "$@"
else
    flask run --host=0.0.0.0
fi

#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python /opt/project/manage.py create_db

# Initialize the migration repository (only needed the first time)
flask db init
# Create a migration script
flask db migrate -m "Initial migration"
# Apply the migration
flask db upgrade

python manage.py seed_db
python manage.py create_admin

# If additional command-line arguments are provided, execute them.
# Otherwise, run the Flask development server.
if [ $# -gt 0 ]; then
    exec "$@"
else
    flask run --host=0.0.0.0
fi

#Overview

This Flask-based web application provides an API for managing companies, users, teams, and admins.
The application supports authentication using JWT tokens and has Swagger-based documentation.

##Project Structure

    project_root/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config.py
    │   ├── models.py
    │   ├── extensions.py
    │   ├── views.py
    │
    ├── .env.dev
    ├── Dockerfile
    ├── entrypoint.sh
    ├── manage.py
    ├── requirements.txt 
    └── docker-compose.yml

##Main Modules
**main.py**: Contains the main entry point for running the application.  
**config.py**: Contains configuration settings for the application.  
**models.py**: Contains the database models for the application.  
**extensions.py**: Contains Flask extensions like JWTManager, Migrate, and Api.  
**views.py**: Contains the Flask-RESTx namespaces and routes for the API endpoints.

##Installation
To set up and run the application locally, follow these steps:  

###Install the required dependencies:

    pip install -r requirements.txt

###Set up the environment variables:

    export FLASK_APP=app.main
    export FLASK_ENV=development

###Initialize the database:

    flask db init
    flask db migrate
    flask db upgrade

###Run the application:

    flask run

##API Endpoints
###Admin
**POST** /admins/login: Authenticate an admin user.
###Users
**GET** /users/: List all users.
**POST** /users/: Create a new user.
**GET** /users/<int:id>: Get a user by ID.
###Teams
**GET** /teams/: List all teams.
**POST** /teams/: Create a new team.
**GET** /teams/<int:id>: Get a team by ID.

##All endpoints, except for the admin login, require a JWT token for authentication.

For test purposes database is populated on a application creation

default admin login:password is login:password
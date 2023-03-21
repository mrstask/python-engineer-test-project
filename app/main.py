from flask import Flask
from config import Config
from models import db
from extensions import jwt, migrate, api
from views import users, teams, admin

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

api.init_app(app)
api.add_namespace(users)
api.add_namespace(teams)
api.add_namespace(admin)

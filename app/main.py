from flask import Flask
from app.config import Config
from app.models import db
from app.extensions import jwt, migrate, api
from app.views import users, teams, admin

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

api.init_app(app)
api.add_namespace(users)
api.add_namespace(teams)
api.add_namespace(admin)

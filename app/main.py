from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_restx import Resource, fields, Namespace, Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config.from_object("app.config.Config")
jwt = JWTManager(app)

restx_api = Api(app, version="1.0", title="Your API Title",
                description="Your API Description")
teams = Namespace('teams', description='Team management operations')
users = Namespace('users', description='User management operations')
admin = Namespace('admins', description='Admin management operations')

db = SQLAlchemy(app)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    company = db.relationship("Company", backref=db.backref("users", lazy=True))

    def __init__(self, name, email, company):
        self.name = name
        self.email = email
        self.company = company


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    company = db.relationship("Company", backref=db.backref("teams", lazy=True))

    users = db.relationship(
        "User", secondary="team_user", backref=db.backref("teams", lazy=True)
    )


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

team_user = db.Table(
    "team_user",
    db.Column("team_id", db.Integer, db.ForeignKey("team.id"),
              primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"),
              primary_key=True),
)

team = teams.model('Team', {
    'id': fields.Integer(readOnly=True,
                         description='The team unique identifier'),
    'name': fields.String(required=True, description='The team name'),
    'company_id': fields.Integer(required=True,
                                 description='The company unique identifier'),
    'user_ids': fields.List(fields.Integer,
                            description='List of user unique identifiers')
})

user_model = users.model('User', {
    'id': fields.Integer(readOnly=True,
                         description='The user unique identifier'),
    'name': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
    'company_id': fields.Integer(required=True,
                                 description='The company unique identifier')
})

@jwt_required()
@users.route('/')  # Add a new route to the namespace
class UserList(Resource):
    @users.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = User.query.all()
        return users

    @users.expect(user_model)
    @users.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.json
        company = Company.query.get(data['company_id'])
        if not company:
            return {"message": "Company not found"}, 404

        user = User(name=data['name'], email=data['email'], company=company)
        db.session.add(user)
        db.session.commit()
        return user, 201

@jwt_required()
@users.route('/<int:id>')
@users.response(404, 'User not found')
@users.param('id', 'The user unique identifier')
class UserResource(Resource):
    @teams.marshal_with(user_model)
    def get(self, id):
        """Get a user by ID"""
        user = User.query.get(id)
        if not user:
            return {"message": "User not found"}, 404
        return user

@jwt_required()
@teams.route('/')
class TeamList(Resource):
    @teams.marshal_list_with(team)
    def get(self):
        teams = Team.query.all()
        return teams

    @teams.expect(team)
    @teams.marshal_with(team, code=201)
    def post(self):
        data = request.json
        company = Company.query.get(data['company_id'])
        if not company:
            return {"message": "Company not found"}, 404

        team = Team(name=data['name'], company=company)
        db.session.add(team)
        db.session.flush()

        users = User.query.filter(User.id.in_(data['user_ids'])).all()
        for user in users:
            team.users.append(user)

        db.session.commit()
        return team, 201

@jwt_required()
@teams.route('/<int:id>')
@teams.response(404, 'Team not found')
@teams.param('id', 'The team unique identifier')
class TeamResource(Resource):
    @teams.marshal_with(team)
    def get(self, id):
        team = Team.query.get(id)
        if not team:
            return {"message": "Team not found"}, 404
        return team


@admin.route("/login")
class AdminLogin(Resource):
    @admin.expect(admin.model("AdminLogin", {
        "username": fields.String(required=True),
        "password": fields.String(required=True)
    }))
    def post(self):
        data = request.json
        admin = Admin.query.filter_by(username=data["username"]).first()

        if admin and check_password_hash(admin.password, data["password"]):
            access_token = create_access_token(identity=admin.id)
            return {"access_token": access_token}, 200
        else:
            return {"message": "Invalid username or password"}, 401


# Register the namespace
restx_api.add_namespace(admin)
restx_api.add_namespace(teams)
restx_api.add_namespace(users)

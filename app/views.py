from flask_restx import Resource, fields
from flask import request

from app.models import Team, User, Company, Admin, db
from app.serializers import teams, users, admin, user_model, team
from app.extensions import api
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash


@users.route("/")  # Add a new route to the namespace
class UserList(Resource):
    @jwt_required()
    @api.doc(security="Bearer")
    @users.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = User.query.all()
        return users

    @jwt_required()
    @api.doc(security="Bearer")
    @users.expect(user_model)
    @users.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.json
        company = Company.query.get(data["company_id"])
        if not company:
            return {"message": "Company not found"}, 404

        user = User(name=data["name"], email=data["email"], company=company)
        db.session.add(user)
        db.session.commit()
        return user, 201


@users.route("/<int:id>")
@users.response(404, "User not found")
@users.param("id", "The user unique identifier")
class UserResource(Resource):
    @jwt_required()
    @api.doc(security="Bearer")
    @teams.marshal_with(user_model)
    def get(self, id):
        """Get a user by ID"""
        user = User.query.get(id)
        if not user:
            return {"message": "User not found"}, 404
        return user


@teams.route("/")
class TeamList(Resource):
    def _team_to_dict(self, team):
        return {
            "id": team.id,
            "name": team.name,
            "company_id": team.company_id,
            "user_ids": [user.id for user in team.users],
        }

    @jwt_required()
    @api.doc(security="Bearer")
    @teams.marshal_list_with(team)
    def get(self):
        teams = Team.query.all()
        result = [self._team_to_dict(team) for team in teams]
        return result

    @jwt_required()
    @api.doc(security="Bearer")
    @teams.expect(team)
    @teams.marshal_with(team, code=201)
    def post(self):
        data = request.json
        company = Company.query.get(data["company_id"])
        if not company:
            return {"message": "Company not found"}, 404

        team = Team(name=data["name"], company=company)
        db.session.add(team)
        db.session.flush()

        users = User.query.filter(User.id.in_(data["user_ids"])).all()
        for user in users:
            team.users.append(user)

        db.session.commit()
        return self._team_to_dict(team), 201


@teams.route("/<int:id>")
@teams.response(404, "Team not found")
@teams.param("id", "The team unique identifier")
class TeamResource(Resource):
    def _team_to_dict(self, team):
        return {
            "id": team.id,
            "name": team.name,
            "company_id": team.company_id,
            "user_ids": [user.id for user in team.users],
        }

    @jwt_required()
    @api.doc(security="Bearer")
    @teams.marshal_with(team)
    def get(self, id):
        team = Team.query.get(id)
        if not team:
            return {"message": "Team not found"}, 404
        return self._team_to_dict(team)


@admin.route("/login")
class AdminLogin(Resource):
    @admin.expect(
        admin.model(
            "AdminLogin",
            {
                "username": fields.String(required=True),
                "password": fields.String(required=True),
            },
        )
    )
    def post(self):
        data = request.json
        admin = Admin.query.filter_by(username=data["username"]).first()

        if admin and check_password_hash(admin.password, data["password"]):
            access_token = create_access_token(identity=admin.id)
            return {"access_token": access_token}, 200
        else:
            return {"message": "Invalid username or password"}, 401

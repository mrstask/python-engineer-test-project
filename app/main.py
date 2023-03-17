from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("app.config.Config")

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


team_user = db.Table(
    "team_user",
    db.Column("team_id", db.Integer, db.ForeignKey("team.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

from flask import request
from flask_restx import Resource, fields, Namespace

api = Namespace('teams', description='Team management operations')

team = api.model('Team', {
    'id': fields.Integer(readOnly=True,
                         description='The team unique identifier'),
    'name': fields.String(required=True, description='The team name'),
    'company_id': fields.Integer(required=True,
                                 description='The company unique identifier'),
    'user_ids': fields.List(fields.Integer,
                            description='List of user unique identifiers')
})

team = api.model('Team', {
    'id': fields.Integer(readOnly=True,
                         description='The team unique identifier'),
    'name': fields.String(required=True, description='The team name'),
    'company_id': fields.Integer(required=True,
                                 description='The company unique identifier'),
    'user_ids': fields.List(fields.Integer,
                            description='List of user unique identifiers')
})


@api.route('/')
class TeamList(Resource):
    @api.marshal_list_with(team)
    def get(self):
        teams = Team.query.all()
        return teams

    @api.expect(team)
    @api.marshal_with(team, code=201)
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


@api.route('/<int:id>')
@api.response(404, 'Team not found')
@api.param('id', 'The team unique identifier')
class TeamResource(Resource):
    @api.marshal_with(team)
    def get(self, id):
        team = Team.query.get(id)
        if not team:
            return {"message": "Team not found"}, 404
        return team

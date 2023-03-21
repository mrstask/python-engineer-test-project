from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


team_user = db.Table(
    "team_user",
    db.Column("team_id", db.Integer, db.ForeignKey("team.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

import random
from flask.cli import FlaskGroup

from app.main import app, db, User, Company, Team, Admin

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    # Seed 10 companies
    companies = []
    for i in range(10):
        company = Company(name=f"Company {i + 1}")
        db.session.add(company)
        companies.append(company)

    db.session.commit()

    # Seed 10 users
    users = []
    for i in range(10):
        user = User(
            name=f"User {i + 1}",
            email=f"user{i + 1}@example.com",
            company=random.choice(companies),
        )
        db.session.add(user)
        users.append(user)

    db.session.commit()

    # Seed 2 teams
    teams = []
    for i in range(2):
        team = Team(name=f"Team {i + 1}", company=random.choice(companies))
        team.users = random.sample(users, k=len(users))
        db.session.add(team)
        teams.append(team)

    db.session.commit()


@cli.command("create_admin")
def create_admin():
    admin = Admin(username='username', password='password')
    db.session.add(admin)
    db.session.commit()


if __name__ == "__main__":
    cli()

from flask_restx import Namespace, fields


teams = Namespace("teams", description="Team management operations")
users = Namespace("users", description="User management operations")
admin = Namespace("admins", description="Admin management operations")


team = teams.model(
    "Team",
    {
        "id": fields.Integer(readOnly=True, description="The team unique identifier"),
        "name": fields.String(required=True, description="The team name"),
        "company_id": fields.Integer(
            required=True, description="The company unique identifier"
        ),
        "user_ids": fields.List(
            fields.Integer, description="List of user unique identifiers"
        ),
    },
)

user_model = users.model(
    "User",
    {
        "id": fields.Integer(readOnly=True, description="The user unique identifier"),
        "name": fields.String(required=True, description="The user name"),
        "email": fields.String(required=True, description="The user email"),
        "company_id": fields.Integer(
            required=True, description="The company unique identifier"
        ),
    },
)

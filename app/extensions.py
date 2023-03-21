from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api

jwt = JWTManager()
migrate = Migrate()
api = Api(
    version="1.0",
    title="Your API Title",
    description="A description of your API",
    doc="/swagger/",
    authorizations={
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": 'Please enter the word "Bearer" followed by a space and your JWT token in the text field below.',
        }
    },
    security="Bearer",
)

import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCK_LIST
import models

from resources.items import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.users import blp as UsersBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Sotores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "00134cloneFistBites!"

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCK_LIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
            {
                "description": "The token has been revoked.",
                "error": "token_revoked"
            }
            ),
            401
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                "description": "The token is not fresh.",
                "error": "fresh_toek_required"
                }
            ),
            401
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Token has expired", "error": "token_expired"}),
            401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": "Signature verification failed.", 
                "error": "invalid_token"
                }),
            401
        )

    @jwt.invalid_token_loader
    def missing_token_callback(error):
        return (
            jsonify({"description": "Request does not contain an access token.", 
                     "error": "invalid_token"}),
            401
        )
    '''
    in terminal 
    flask db init 
    after
    flask db migrate
    to upgrade
    flask db upgrade
    You add a new column o relashioship or new table
    flask db migrate
    flask db upgrade
    with app.app_context():
        db.create_all()
    '''

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    app.register_blueprint(UsersBlueprint)

    return app

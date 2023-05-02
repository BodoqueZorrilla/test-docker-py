import os
import requests
from flask import current_app
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, create_refresh_token, get_jwt_identity

from db import db
from schemas import UserSchema, UserRegisterSchema
from models import UserModel
from blocklist import BLOCK_LIST
from tasks import send_user_registartion_email

blp = Blueprint("Users", __name__, "Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
                or_(
                    UserModel.username == user_data["username"],
                    UserModel.email == user_data["email"]
                )
            ).first():
            abort(409,
                  "A user with tath username already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        current_app.queue.enqueue(send_user_registartion_email, user.email, user.username)
        '''
        send_simple_email()
        '''

        return { "message": "User creadet successfully"}
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, "Invalid Credentials")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCK_LIST.add(jti)
        return {"message": "Successfully logged out."}


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted"}, 200
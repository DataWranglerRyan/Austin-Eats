from flask import session
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from common.utils import Utils
from models.user_model import UserModel


# Resources are external representation of a Object. It interacts with API.
class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'user_name',
        required=True,
        type=str,
        help='Field is required.'
    )
    parse.add_argument(
        'password',
        required=True,
        type=str,
        help='Field is required.'
    )

    @staticmethod
    def post():
        data = UserRegister.parse.parse_args()
        encrypted_pw = Utils.encrypt_password(data['password'])
        if UserModel.find_by_username(data['user_name']):
            return {'msg': 'User already exists.'}, 400

        UserModel(user_name=data['user_name'], password=encrypted_pw).save_to_db()
        return {'msg': 'User created'}, 201

    # @staticmethod
    # def delete():
    #     data = UserRegister.parse.parse_args()
    #     user = UserModel.find_by_username(data['user_name'])
    #     if not user:
    #         return {'msg': 'User does not exists.'}, 400
    #
    #     user.delete_from_db()
    #     return {'msg': 'User Deleted'}, 200


class UserLogin(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'user_name',
        required=True,
        type=str,
        help='Field is required.'
    )
    parse.add_argument(
        'password',
        required=True,
        type=str,
        help='Field is required.'
    )

    @staticmethod
    def authenticate(user_name, password):
        if not user_name:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400
        user = UserModel.find_by_username(user_name)
        if not user:
            return {"msg": "No User Found"}, 401
        if not Utils.check_encrypted_password(password, user.password):
            return {"msg": "Incorrect Password"}, 401
        else:
            return {"token": create_access_token(identity=user.username), "user_name": user_name}, 200

    @staticmethod
    def login(user_name):
        session['user_name'] = user_name

    @staticmethod
    def logout():
        session['user_name'] = None

    def post(self):
        data = UserLogin.parse.parse_args()
        return self.authenticate(data['user_name'], data['password'])

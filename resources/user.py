from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
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

    def post(self):
        data = UserRegister.parse.parse_args()
        if UserModel.find_by_username(data['user_name']):
            return {'msg': 'User already exists.'}, 400

        UserModel(**data).save_to_db()
        return {'msg': 'User created'}, 201


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
        if not safe_str_cmp(user.password, password):
            return {"msg": "Incorrect Password"}, 401
        else:
            return {"token": create_access_token(identity=user.username)}, 200

    def post(self):
        data = UserLogin.parse.parse_args()
        return self.authenticate(data['user_name'], data['password'])

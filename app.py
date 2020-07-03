import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserLogin
from resources.restaurant import Restaurant, RestaurantList
from resources.dish import Dish, DishList
from models.restaurant_model import RestaurantModel


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['JWT_SECRET_KEY'] = 'ryan'
jwt = JWTManager(app)
api = Api(app)


# @app.before_first_request
# def create_tables():
#     db.create_all()
#     if not RestaurantModel.find_by_name('Sugar Pine'):
#         RestaurantModel('Sugar Pine', 3.75).save_to_db()


api.add_resource(Restaurant, '/restaurant/<string:name>')
api.add_resource(RestaurantList, '/restaurants')
api.add_resource(Dish, '/dish/<string:name>')
api.add_resource(DishList, '/dishes')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

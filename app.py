import os
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserLogin
from resources.restaurant import Restaurant, RestaurantList
from resources.dish import Dish, DishList, DishByRestaurantID, DishListByRestaurantID
from controllers.restaurants_blueprint import restaurant_blueprint, restaurants_blueprint
from controllers.user_auth_blueprint import user_register_blueprint, user_login_blueprint


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['JWT_SECRET_KEY'] = 'ryan'
app.secret_key = 'ryan'
jwt = JWTManager(app)


app.register_blueprint(user_login_blueprint, url_prefix='/login')
app.register_blueprint(user_register_blueprint, url_prefix='/register')
app.register_blueprint(restaurants_blueprint, url_prefix='/restaurants')
app.register_blueprint(restaurant_blueprint, url_prefix='/restaurant')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


api = Api(app, prefix='/api')
api.add_resource(Restaurant, '/restaurant/<string:name>')
api.add_resource(RestaurantList, '/restaurants')
api.add_resource(Dish, '/dish/<string:name>')
api.add_resource(DishByRestaurantID, '/restaurant/<string:restaurant_id>/dish')
api.add_resource(DishList, '/dishes')
api.add_resource(DishListByRestaurantID, '/restaurant/<string:restaurant_id>/dishes')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)


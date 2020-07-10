import os
from flask import Flask, render_template, request, session, make_response
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserLogin
from resources.restaurant import Restaurant, RestaurantList
from resources.dish import Dish, DishList, DishByRestaurantID, DishListByRestaurantID


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['JWT_SECRET_KEY'] = 'ryan'
app.secret_key = 'ryan'
jwt = JWTManager(app)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        payload, status_code = UserLogin.authenticate(user_name, password)
        if status_code == 200:
            UserLogin.login(user_name)
            return render_template('profile.html', username=session['user_name'])
        else:
            UserLogin.logout()
            return render_template('error.html', error=payload.get('msg'))


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_user():
    user_name = request.form['user_name']
    payload, status_code = UserRegister.post()
    if status_code == 201:
        UserLogin.login(user_name)
        return render_template('profile.html', username=session['user_name'])
    else:
        UserLogin.logout()
        return render_template('error.html', error=payload.get('msg'))


@app.route('/restaurants', methods=['GET'])
def restaurant_list():
    if session.get('user_name'):
        payload, status_code = RestaurantList.get()
        return render_template('restaurants.html', restaurants=payload['restaurants'])
    else:
        return render_template('error.html', error='Please Login.')


@app.route('/restaurant/<string:name>', methods=['GET'])
def restaurant_by_name(name):
    if session.get('user_name'):
        payload, status_code = Restaurant.get(name)
        if status_code == 200:
            return render_template('restaurant.html', restaurant=payload)
        else:
            return render_template('error.html', error=payload['message'])
    else:
        return render_template('error.html', error='Please Login.')


@app.route('/restaurant/new', methods=['POST', 'GET'])
def create_restaurant():
    if request.method == 'GET':
        return render_template('new_restaurant.html')
    else:
        Restaurant.post(request.form['name'])
        return make_response(restaurant_list())


@app.route('/restaurant/<string:restaurant_id>/dish/new', methods=['POST', 'GET'])
def create_restaurant_dish(restaurant_id):
    if request.method == 'GET':
        return render_template('new_restaurant_dish.html', restaurant_id=restaurant_id)
    else:
        DishByRestaurantID.post(restaurant_id)
        # NEED TO Return to restaurant view not restaurants
        return make_response(restaurant_list())


api.add_resource(Restaurant, '/api/restaurant/<string:name>')
api.add_resource(RestaurantList, '/api/restaurants')
api.add_resource(Dish, '/api/dish/<string:name>')
api.add_resource(DishByRestaurantID, '/api/restaurant/<string:restaurant_id>/dish')
api.add_resource(DishList, '/api/dishes')
api.add_resource(DishListByRestaurantID, '/api/restaurant/<string:restaurant_id>/dishes')
api.add_resource(UserRegister, '/api/register')
api.add_resource(UserLogin, '/api/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

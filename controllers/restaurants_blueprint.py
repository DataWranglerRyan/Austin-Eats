from flask import Blueprint, render_template, make_response, request, session
from resources.restaurant import Restaurant, RestaurantList, RestaurantByID
from resources.dish import DishByRestaurantID, DishListByRestaurantID

restaurants_blueprint = Blueprint('restaurants', __name__)
restaurant_blueprint = Blueprint('restaurant', __name__)

# RESTAURANTS ################


@restaurants_blueprint.route('/', methods=['GET'])
def restaurant_list():
    if session.get('user_name'):
        payload, status_code = RestaurantList.get()
        return render_template('restaurant/index.html', restaurants=payload['restaurants'],
                               user_name=session['user_name'], restaurant=Restaurant)
    else:
        return render_template('error.html', error='Please Login.')

# RESTAURANT ################


@restaurant_blueprint.route('/<string:name>', methods=['GET'])
def restaurant_by_name(name):
    if session.get('user_name'):
        payload, status_code = Restaurant.get(name)
        payload.update(DishListByRestaurantID.get(payload['id'])[0])
        if status_code == 200:
            return render_template('restaurant/restaurant.html', restaurant=payload)
        else:
            return render_template('error.html', error=payload['message'])
    else:
        return render_template('error.html', error='Please Login.')


@restaurant_blueprint.route('/new', methods=['POST', 'GET'])
def create_restaurant():
    if request.method == 'GET':
        return render_template('restaurant/new.html')
    else:
        Restaurant.post(request.form['name'])
        return make_response(restaurant_list())


@restaurant_blueprint.route('/<string:restaurant_id>/dish/new', methods=['POST', 'GET'])
def create_restaurant_dish(restaurant_id):
    if request.method == 'GET':
        return render_template('restaurant/dish/new.html', restaurant_id=restaurant_id)
    else:
        DishByRestaurantID.post(restaurant_id)
        payload, status_code = RestaurantByID.get(restaurant_id)
        return render_template('restaurant/restaurant.html', restaurant=payload)

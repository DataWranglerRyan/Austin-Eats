from flask import Blueprint, render_template, request, session, redirect, url_for
from resources.restaurant import Restaurant, RestaurantList, RestaurantByID, RestaurantGetRandom
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


@restaurant_blueprint.route('/random', methods=['GET'])
def get_random():
    payload, status_code = RestaurantGetRandom.get()
    if status_code == 200:
        return redirect(url_for(".restaurant_by_name", name=payload['name']))
    else:
        return render_template('error.html', error=payload['message'])


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
        return redirect(url_for("restaurants.restaurant_list"))


@restaurant_blueprint.route('/edit/<string:restaurant_id>', methods=['POST', 'GET'])
def edit_restaurant(restaurant_id):
    payload, status_code = RestaurantByID.get(restaurant_id)
    if request.method == 'POST':
        Restaurant.put(payload['name'])
        return redirect(url_for("restaurants.restaurant_list", name=payload['name']))
    else:
        return render_template("restaurant/edit.html", restaurant=payload)


@restaurant_blueprint.route('/<string:restaurant_id>/dish/new', methods=['POST', 'GET'])
def create_restaurant_dish(restaurant_id):
    if request.method == 'GET':
        return render_template('restaurant/dish/new.html', restaurant_id=restaurant_id)
    else:
        DishByRestaurantID.post(restaurant_id)
        payload, status_code = RestaurantByID.get(restaurant_id)
        return redirect(url_for(".restaurant_by_name", name=payload['name']))

from flask import Blueprint, redirect, url_for
from resources.restaurant import RestaurantByID
from resources.dish import DishByID


dish_blueprint = Blueprint('dish', __name__)


@dish_blueprint.route('/delete/<string:dish_id>', methods=['GET'])
def delete_dish(dish_id):
    dish, dish_status_code = DishByID.get(dish_id)
    restaurant, restaurant_status_code = RestaurantByID.get(dish['restaurant_id'])
    DishByID.delete(dish_id)
    return redirect(url_for("restaurant.restaurant_by_name", name=restaurant['name']))

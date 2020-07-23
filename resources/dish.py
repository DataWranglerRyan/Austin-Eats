from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from typing import Dict
from models.dish_model import DishModel
from models.restaurant_model import RestaurantModel


class Dish(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'review',
        required=True,
        type=float,
        help='Every dish needs a review'
    )
    parse.add_argument(
        'restaurant_id',
        required=True,
        type=float,
        help='Every dish needs a restaurant id.'
    )

    @jwt_required
    def get(self, name) -> (Dict, int):
        dish = DishModel.find_by_name(name)
        if dish:
            return dish.json(), 200
        return {'message': 'Dish not found.'}, 404  # return 404 Not Found

    @classmethod
    def post(cls, name) -> (Dict, int):
        if DishModel.find_by_name(name):
            return {'message': f'Dish with name {name} already exists.'}, 400

        payload = cls.parse.parse_args()
        dish = DishModel(name, payload['review'], payload['restaurant_id'])

        try:
            dish.save_to_db()
        except Exception as e:
            {'message': 'An error occurred'}, 500

        return dish.json(), 201  # return 201 Created

    @staticmethod
    def delete(name) -> (Dict, int):
        dish = DishModel.find_by_name(name)
        if dish:
            dish.delete_from_db()
            return {'message': f'{name} deleted.'}, 200
        else:
            return {'message': f'Dish ({name}) does not exist.'}, 400

    @classmethod
    def put(cls, name) -> (Dict, int):
        payload = cls.parse.parse_args()
        dish = DishModel.find_by_name(name)

        if dish is None:
            try:
                dish = DishModel(name, payload['review'], payload['restaurant_id'])
            except:
                return {'message': 'An error occurred creating Dish.'}, 500
        else:
            try:
                dish.review = payload['review']
            except:
                return {'message': 'An error occurred updating Dish.'}, 500

        dish.save_to_db()
        return dish.json(), 200


class DishByID(Resource):
    @staticmethod
    def get(dish_id) -> (Dict, int):
        dish = DishModel.find_by_id(dish_id)
        if dish:
            return dish.json(), 200
        return {'message': 'Dish not found.'}, 404  # return 404 Not Found

    @staticmethod
    def delete(dish_id) -> (Dict, int):
        dish = DishModel.find_by_id(dish_id)
        if dish:
            dish.delete_from_db()
            return {'message': f'{dish.name} deleted.'}, 200
        else:
            return {'message': f'Dish ({dish.name}) does not exist.'}, 400


class DishByRestaurantID(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'review',
        required=True,
        type=float,
        help='Every dish by restaurant id needs a review.'
    )
    parse.add_argument(
        'name',
        required=True,
        type=str,
        help='Every dish by restaurant id needs a name.'
    )

    @classmethod
    def post(cls, restaurant_id) -> (Dict, int):
        if not RestaurantModel.find_by_id(restaurant_id):
            return {'message': f'Cannot add dish. Restaurant with {restaurant_id} does not exist. '}, 400
        payload = cls.parse.parse_args()
        dish = DishModel(payload['name'], payload['review'], restaurant_id)

        try:
            dish.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred'}, 500

        return dish.json(), 201  # return 201 Created


class DishList(Resource):
    @jwt_required
    def get(self) -> (Dict, int):
        return {'dishes': [d.json() for d in DishModel.get_all()]}, 200


class DishListByRestaurantID(Resource):
    @staticmethod
    def get(restaurant_id) -> (Dict, int):
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if not restaurant:
            return {'message': f'Cannot get Dishes. Restaurant with {restaurant_id} does not exist. '}, 400

        dishes = restaurant.get_dishes()
        if dishes:
            return {'restaurant': f'/api/restaurant/id/{restaurant_id}',
                    'dishes': [d.json(show_restaurant=False) for d in dishes]}, 200
        return {'dishes': [], 'message': 'Restaurant has no dishes.'}, 404  # return 404 Not Found


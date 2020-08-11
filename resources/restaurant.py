from flask import session
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from typing import Dict
from models.restaurant_model import RestaurantModel
from models.user_model import UserModel
from models.restaurant_review_model import RestaurantReviewModel


class Restaurant(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'review',
        required=True,
        type=float,
        help='Field is required.'
    )
    parse.add_argument(
        'user_name',
        required=False,
        type=str,
        help='Field is Optional, but should be used for POST and PUT.'
    )

    @staticmethod
    def get_random() -> Dict:
        restaurant = RestaurantModel.get_random()
        if restaurant:
            return restaurant.json()
        else:
            return {'message': "No Restaurants. Can't get random."}

    @staticmethod
    # @jwt_required
    def get(name) -> (Dict, int):
        restaurant = RestaurantModel.find_by_name(name)
        if restaurant:
            return restaurant.json(), 200
        return {'message': 'Restaurant not found.'}, 404  # return 404 Not Found

    @staticmethod
    # @jwt_required
    def post(name) -> (Dict, int):
        payload = Restaurant.parse.parse_args()
        added_by = session.get('user_name', payload.get('user_name'))
        existing_restaurant = RestaurantModel.find_by_name(name)
        new_restaurant = RestaurantModel(name, added_by)
        restaurant = existing_restaurant if existing_restaurant else new_restaurant
        review = RestaurantReviewModel(payload['review'])
        user = UserModel.find_by_username(added_by)
        if user.has_specific_restaurant(restaurant):
            return {'message': f'User already has restaurant with name {name}'}, 400
        else:
            user.reviews.append(review)
            restaurant.reviews.append(review)
            restaurant.users.append(user)

        try:
            restaurant.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred'}, 500

        return restaurant.json(), 201  # return 201 Created

    @staticmethod
    def delete(name) -> (Dict, int):
        restaurant = RestaurantModel.find_by_name(name)
        if restaurant:
            restaurant.delete_from_db()
            return {'message': '{} deleted.'.format(name)}, 200
        else:
            return {'message': f'Restaurant ({name}) does not exist.'}, 400

    @staticmethod
    def put(name) -> (Dict, int):
        payload = Restaurant.parse.parse_args()
        restaurant = RestaurantModel.find_by_name(name)

        if restaurant is None:
            return Restaurant.post(name)
        else:
            try:
                user = UserModel.find_by_username(session.get('user_name', payload.get('user_name')))
                review = restaurant.get_review_by_user_id(user.id)
                review.review = payload['review']
                review.save_to_db()
            except:
                return {'message': 'An error occurred updating restaurant.'}, 500
        return restaurant.json(), 200


class RestaurantByID(Resource):
    @staticmethod
    # @jwt_required
    def get(restaurant_id) -> (Dict, int):
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if restaurant:
            return restaurant.json(), 200
        return {'message': 'Restaurant not found.'}, 404  # return 404 Not Found

    @staticmethod
    def delete(restaurant_id) -> (Dict, int):
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if restaurant:
            restaurant.delete_from_db()
            return {'message': '{} deleted.'.format(restaurant.name)}, 200
        else:
            return {'message': f'Restaurant ({restaurant.name}) does not exist.'}, 400


class RestaurantGetRandom(Resource):
    @staticmethod
    def get() -> (Dict, int):
        restaurant = RestaurantModel.get_random()
        if restaurant:
            return restaurant.json(), 200
        return {'message': 'Random Restaurant not found.'}, 404  # return 404 Not Found


class RestaurantList(Resource):
    @staticmethod
    # @jwt_required
    def get() -> (Dict, int):
        return {'restaurants': [r.json() for r in RestaurantModel.get_all()]}, 200


class RestaurantListByUser(Resource):
    @staticmethod
    def get(user_name) -> (Dict, int):
        user = UserModel.find_by_username(user_name)
        return {'restaurants': [r.json() for r in user.get_restaurants()]}, 200


class RestaurantByUser(Resource):
    @staticmethod
    def delete(user_name, restaurant_id) -> (Dict, int):
        user = UserModel.find_by_username(user_name)
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        user.restaurants.remove(restaurant)
        # REMOVE reviews by Restaurant isnt working 100%. Doesn't delete all reviews. CHECK.
        user.remove_reviews_by_restaurant_id(restaurant.id)
        user.save_to_db()
        return {'restaurants': [r.json() for r in user.get_restaurants()]}, 200

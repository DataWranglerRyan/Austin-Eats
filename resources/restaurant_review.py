from flask import session
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from typing import Dict
from models.restaurant_model import RestaurantModel
from models.restaurant_review_model import RestaurantReviewModel


class RestaurantReview(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'review',
        required=True,
        type=float,
        help='Field is required.'
    )
    parse.add_argument(
        'comment',
        required=False,
        type=str,
        help='Field is Optional.'
    )

    @staticmethod
    def get(restaurant_id) -> (Dict, int):
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if not restaurant:
            return {'message': 'Restaurant not found.'}, 404
        reviews = restaurant.reviews
        if reviews:
            return {'reviews': [r.json() for r in reviews]}, 200
        return {'message': 'No Reviews found.'}, 404

    @classmethod
    def post(cls, restaurant_id) -> (Dict, int):
        payload = cls.parse.parse_args()
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if not restaurant:
            return {'message': 'Restaurant not found.'}, 404
        review = RestaurantReviewModel(review=payload['review'], comment=payload['comment'],
                                       reviewer=session.get('user_name', 'api_user'))
        review.restaurant = restaurant
        try:
            review.save_to_db()
        except Exception as e:
            return {'message': f'An error occurred. {e}'}, 500

        return review.json(), 201  # return 201 Created


# class RestaurantReviewByID(Resource):
#     @classmethod
#     def put(cls, restaurant_id) -> (Dict, int):
#         payload = cls.parse.parse_args()
#         restaurant = RestaurantModel.find_by_id(restaurant_id)
#         if not restaurant:
#             return {'message': 'Restaurant not found.'}, 404
#
#         review = restaurant.get_review_by_id()
#
#         if review is None:
#             try:
#                 review = RestaurantReviewModel(payload['review'], payload['comment'], payload['reviewer'])
#                 review.restaurant = restaurant
#             except Exception as e:
#                 return {'message': f'An error occurred creating Review.'}, 500
#         else:
#             try:
#                 review.review = payload['review']
#                 review.comment = payload['comment']
#             except Exception as e:
#                 return {'message': f'An error occurred updating Review.'}, 500
#
#         review.save_to_db()
#         return review.json(), 200



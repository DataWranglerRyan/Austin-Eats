from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.dish_model import DishModel


class Dish(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'review',
        required=True,
        type=float,
        help='Field is required.'
    )
    parse.add_argument(
        'restaurant_id',
        required=True,
        type=float,
        help='Every dish needs a restaurant id.'
    )

    @jwt_required
    def get(self, name):
        dish = DishModel.find_by_name(name)
        if dish:
            return dish.json(), 200
        return {'message': 'Dish not found.'}, 404  # return 404 Not Found

    def post(self, name):
        if DishModel.find_by_name(name):
            return {'message': 'Dish with name {} already exists.'.format(name)}, 400

        payload = Dish.parse.parse_args()
        dish = DishModel(name, payload['review'], payload['restaurant_id'])

        try:
            dish.save_to_db()
        except Exception as e:
            {'message': 'An error occurred'}, 500

        return dish.json(), 201  # return 201 Created

    def delete(self, name):
        dish = DishModel.find_by_name(name)
        if dish:
            dish.delete_from_db()
            return {'message': '{} deleted.'.format(name)}, 200
        else:
            return {'message': 'Restaurant does not exist.'.format(name)}, 400

    def put(self, name):
        payload = Dish.parse.parse_args()
        dish = DishModel.find_by_name(name)

        if dish is None:
            try:
                dish = DishModel(name, payload['review'], payload['restaurant_id'])
            except:
                {'message': 'An error occurred creating restaurant.'}, 500
        else:
            try:
                dish.review = payload['review']
            except:
                {'message': 'An error occurred updating restaurant.'}, 500

        dish.save_to_db()
        return dish.json(), 200


class DishList(Resource):
    @jwt_required
    def get(self):
        return {'dishes': [r.json() for r in DishModel.get_all()]}, 200


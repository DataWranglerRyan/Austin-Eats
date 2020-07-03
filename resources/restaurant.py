from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.restaurant_model import RestaurantModel


class Restaurant(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'review',
        required=True,
        type=float,
        help='Field is required.'
    )

    @jwt_required
    def get(self, name):
        restaurant = RestaurantModel.find_by_name(name)
        if restaurant:
            return restaurant.json(), 200
        return {'message': 'Restaurant not found.'}, 404  # return 404 Not Found

    def post(self, name):
        if RestaurantModel.find_by_name(name):
            return {'message': 'Restaurant with name {} already exists.'.format(name)}, 400

        payload = Restaurant.parse.parse_args()
        restaurant = RestaurantModel(name, payload['review'])

        try:
            restaurant.save_to_db()
        except Exception as e:
            {'message': 'An error occurred'}, 500

        return restaurant.json(), 201  # return 201 Created

    def delete(self, name):
        restaurant = RestaurantModel.find_by_name(name)
        if restaurant:
            restaurant.delete_from_db()
            return {'message': '{} deleted.'.format(name)}, 200
        else:
            return {'message': 'Restaurant does not exist.'.format(name)}, 400

    def put(self, name):
        payload = Restaurant.parse.parse_args()
        restaurant = RestaurantModel.find_by_name(name)

        if restaurant is None:
            try:
                restaurant = RestaurantModel(name, payload['review'])
            except:
                {'message': 'An error occurred creating restaurant.'}, 500
        else:
            try:
                restaurant.review = payload['review']
            except:
                {'message': 'An error occurred updating restaurant.'}, 500

        restaurant.save_to_db()
        return restaurant.json(), 200


class RestaurantList(Resource):
    @jwt_required
    def get(self):
        return {'restaurants': [r.json() for r in RestaurantModel.get_all()]}, 200


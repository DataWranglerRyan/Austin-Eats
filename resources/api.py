from .restaurant import Restaurant, RestaurantByID, RestaurantGetRandom, RestaurantList
from .dish import Dish, DishByID, DishByRestaurantID, DishList, DishListByRestaurantID
from .user import UserRegister, UserLogin


def add_api_resources(api):
    api.add_resource(Restaurant, '/restaurant/<string:name>')
    api.add_resource(RestaurantGetRandom, '/restaurant/random')
    api.add_resource(RestaurantByID, '/restaurant/id/<string:restaurant_id>')
    api.add_resource(RestaurantList, '/restaurants')
    api.add_resource(Dish, '/dish/<string:name>')
    api.add_resource(DishByID, '/dish/id/<string:dish_id>')
    api.add_resource(DishByRestaurantID, '/restaurant/<string:restaurant_id>/dish')
    api.add_resource(DishList, '/dishes')
    api.add_resource(DishListByRestaurantID, '/restaurant/<string:restaurant_id>/dishes')
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
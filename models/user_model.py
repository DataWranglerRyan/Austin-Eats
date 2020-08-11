from db import db
from .restaurant_review_model import RestaurantReviewModel


# Models are internal representation of a Object. It is a helper for us, but the API does not interact with the API.
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Auto Increments
    username = db.Column(db.String(80))
    password = db.Column(db.String(512))

    # lazy=dynamic returns a Query object that you can filter, otherwise it would return a list of model objects.
    # See the remove_reviews_by_restaurant_id method for an example of why dynamic was set.
    restaurants = db.relationship('RestaurantModel', secondary='user_restaurants', lazy='dynamic')
    reviews = db.relationship('RestaurantReviewModel', cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, user_name, password):
        self.username = user_name
        self.password = password

    def __str__(self):
        return self.username + ' ' + self.password

    @classmethod
    def login_valid(cls, username, password):
        pass

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def remove_reviews_by_restaurant_id(self, restaurant_id):
        self.reviews = self.reviews.filter(RestaurantReviewModel.restaurant_id != restaurant_id)

    def has_specific_restaurant(self, restaurant):
        return restaurant in self.restaurants

    def get_restaurants(self):
        return self.restaurants

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

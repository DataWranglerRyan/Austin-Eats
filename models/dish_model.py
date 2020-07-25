from db import db
from typing import Dict


class DishModel(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    review = db.Column(db.Float(precision=2))

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('RestaurantModel', back_populates='dishes')

    def __init__(self, name: str, review: float):
        self.name = name
        self.review = review

    def json(self, show_restaurant=True) -> Dict:
        dish_json = {
                    'id': self.id,
                    'name': self.name,
                    'review': self.review
        }
        if show_restaurant:
            dish_json['restaurant_id'] = self.restaurant_id
            dish_json['restaurant'] = f'/api/restaurant/id/{self.restaurant_id}'
        return dish_json

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def from_restaurant(cls, restaurant_id):
        return cls.query.filter_by(restaurant_id=restaurant_id).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        """Inserts or Updates a row in the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

from db import db
from sqlalchemy.sql.expression import func
from typing import Dict, List
from .dish_model import DishModel
from .restaurant_review_model import RestaurantReviewModel


class RestaurantModel(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    review = db.Column(db.Float(precision=2))
    added_by = db.Column(db.String(80))

    dishes = db.relationship('DishModel', back_populates='restaurant', lazy='dynamic')
    reviews = db.relationship('RestaurantReviewModel', back_populates='restaurant', lazy='dynamic')

    def __init__(self, name: str, review: float, added_by: str = None):
        self.name = name
        self.review = review
        self.added_by = added_by

    def json(self) -> Dict:
        return {
                    'id': self.id,
                    'name': self.name,
                    'review': self.review,
                    'dishes': f'/api/restaurant/{self.id}/dishes' #[d.json() for d in self.get_dishes()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def get_random(cls) -> List:
        return cls.query.order_by(func.random()).first()

    def get_dishes(self) -> List:
        return self.dishes.all()

    def get_dish_by_name(self, name):
        return self.dishes.filter(DishModel.name == name).first()

    def get_reviews(self) -> List:
        return self.reviews.all()

    def get_review_by_id(self, review_id):
        return self.reviews.filter(RestaurantReviewModel.id == review_id).first()

    def save_to_db(self):
        """Inserts or Updates a row in the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

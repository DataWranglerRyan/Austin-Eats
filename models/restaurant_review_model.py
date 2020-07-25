from db import db
from sqlalchemy.sql.expression import func
from typing import Dict, List


class RestaurantReviewModel(db.Model):
    __tablename__ = 'restaurant_reviews'

    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Float(precision=2))
    comment = db.Column(db.String(512))
    reviewer = db.Column(db.String(80))

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('RestaurantModel', back_populates='reviews')

    def __init__(self, review: float, comment: str = None, reviewer: str = None):
        self.review = review
        self.comment = comment
        self.reviewer = reviewer

    def json(self) -> Dict:
        return {
                    'review': self.review,
                    'comment': self.comment,
                    'reviewer': self.reviewer,
                    'restaurant_id': self.restaurant_id
        }

    @classmethod
    def find_all_by_reviewer(cls, reviewer):
        return cls.query.filter_by(reviewer=reviewer).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls) -> List:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

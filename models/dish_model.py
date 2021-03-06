from db import db


class DishModel(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    review = db.Column(db.Float(precision=2))

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('RestaurantModel')

    def __init__(self, name, review, restaurant_id):
        self.name = name
        self.review = review
        self.restaurant_id = restaurant_id

    def json(self):
        return {'name': self.name, 'review': self.review}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

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

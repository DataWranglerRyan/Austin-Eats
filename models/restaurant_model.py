from db import db


class RestaurantModel(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    review = db.Column(db.Float(precision=2))

    dishes = db.relationship('DishModel', lazy='dynamic')

    def __init__(self, name, review):
        self.name = name
        self.review = review

    def json(self):
        return {'name': self.name, 'review': self.review, 'dishes': [d.json() for d in self.get_dishes()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def get_dishes(self):
        return self.dishes.all()

    def save_to_db(self):
        """Inserts or Updates a row in the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

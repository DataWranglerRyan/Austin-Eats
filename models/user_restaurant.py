from db import db

user_restaurants = db.Table('user_restaurants',
                            db.Column('id', db.Integer, primary_key=True),
                            db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                            db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurants.id'))
                            )


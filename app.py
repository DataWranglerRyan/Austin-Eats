import os
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.api import add_api_resources
from controllers.restaurants_blueprint import restaurant_blueprint, restaurants_blueprint
from controllers.dish_blueprint import dish_blueprint
from controllers.user_auth_blueprint import user_register_blueprint, user_login_blueprint, user_profile_blueprint


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['JWT_SECRET_KEY'] = 'ryan'
app.secret_key = os.urandom(64)
jwt = JWTManager(app)


app.register_blueprint(user_login_blueprint, url_prefix='/login')
app.register_blueprint(user_register_blueprint, url_prefix='/register')
app.register_blueprint(user_profile_blueprint, url_prefix='/profile')
app.register_blueprint(restaurants_blueprint, url_prefix='/restaurants')
app.register_blueprint(restaurant_blueprint, url_prefix='/restaurant')
app.register_blueprint(dish_blueprint, url_prefix='/dish')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


api = Api(app, prefix='/api')
add_api_resources(api)


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)



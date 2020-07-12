from flask import Blueprint, render_template, request, session
from resources.user import UserLogin, UserRegister

user_login_blueprint = Blueprint('login', __name__)
user_register_blueprint = Blueprint('register', __name__)


@user_login_blueprint.route('', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        payload, status_code = UserLogin.authenticate(user_name, password)
        if status_code == 200:
            UserLogin.login(user_name)
            return render_template('profile.html', username=session['user_name'])
        else:
            UserLogin.logout()
            return render_template('error.html', error=payload.get('msg'))


@user_register_blueprint.route('', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        user_name = request.form['user_name']
        payload, status_code = UserRegister.post()
        if status_code == 201:
            UserLogin.login(user_name)
            return render_template('profile.html', username=session['user_name'])
        else:
            UserLogin.logout()
            return render_template('error.html', error=payload.get('msg'))

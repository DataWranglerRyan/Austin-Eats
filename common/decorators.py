import functools
from typing import Callable
from flask import session, flash, url_for, redirect


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_name'):
            flash('Please sign in to view this page.', 'danger')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function

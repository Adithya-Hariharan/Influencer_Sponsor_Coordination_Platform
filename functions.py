#for simplicity

from functools import wraps
from flask import redirect, url_for, session, flash

def auth_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' in session:
                if session.get('user_role') == required_role:
                    return func(*args, **kwargs)
                else:
                    flash('Access denied: Incorrect role')
                    return redirect(url_for(f'{required_role}_login'))
            else:
                flash('Please login to continue')
                return redirect(url_for(f'{required_role}_login'))
        return wrapper
    return decorator

def logout_required(user_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_role' in session and session['user_role'] == user_role:
                session.pop('user_id', None)
                session.pop('user_role', None)
                flash('You have been logged out.')
                return redirect(url_for(f'{user_role}_login'))
            else:
                flash('You are not logged in or have an incorrect role.')
        return wrapper
    return decorator

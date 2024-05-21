from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from main.models import User
 # Import Role class

login_manager = LoginManager()

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Decorator for role-based access
def role_required(role):
    def wrapper(f):
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.is_admin or current_user.role == role:
                return f(*args, **kwargs)
            else:
                return "Access denied", 403
        return decorated_function
    return wrapper

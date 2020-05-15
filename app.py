# register blueprint and start flask app
from flask import Flask, flash, url_for, redirect
from employee_management import EmployeeViews
from login import UserLoginAuth
from flask_login import LoginManager
from db.db import db
from models.login_models import User
from flask_bootstrap import Bootstrap

app = Flask(__name__, instance_relative_config=False)
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)

app.secret_key = 'asrtarstaursdlarsn'
app.config.from_object('settings.Config')

# initialization
db.init_app(app)

app.register_blueprint(EmployeeViews.employee_app)
app.register_blueprint(UserLoginAuth.login_app)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.filter_by(id = user_id).first()
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login_auth.login'))


# run always put in last statement or put after all @app.route
if __name__ == '__main__':
    app.run(host='localhost')

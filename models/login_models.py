from db.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False, nullable=False)
    last_login = db.Column(db.DateTime, unique=False, nullable=True)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

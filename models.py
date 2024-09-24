from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

# Create the SQLAlchemy instance
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Specify table name if needed

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hash the password and store it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored password hash."""
        return check_password_hash(self.password_hash, password)

class BlenderModel(db.Model):
    __tablename__ = 'blender_models'  # Specify table name if needed

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('blender_models', lazy=True))


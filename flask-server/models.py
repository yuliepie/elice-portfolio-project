from db_connect import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(db.Model):
    """
    Class representing a user of the application.

    Attributes:
        * email (String)
        * hashed password (String)
        * name
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(
        db.String(100), nullable=False, unique=True
    )  # user id must be unique
    password_hashed = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, email: str, password_original: str, name: str):
        self.email = email
        self.password_hashed = bcrypt.generate_password_hash(password_original)
        self.name = name

    def is_password_correct(self, password_original: str):
        return bcrypt.check_password_hash(self.password_hashed, password_original)

    def _repr(self):
        return f"<User: {self.name} {self.email}"

# Create module for blueprints.

from flask import Blueprint

users_blueprint = Blueprint("users", __name__)
user_details_blueprint = Blueprint("user_details", __name__)

from . import users
from . import user_details

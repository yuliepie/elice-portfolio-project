from flask import Blueprint
from models import User
from db_connect import db


users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/")
def index():
    return "Hello World!"


@users_blueprint.route("/test")
def testMigration():
    user = User("aaa", "asdfasdf", "Yulie")
    db.session.add(user)
    db.session.commit()

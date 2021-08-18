from . import users_blueprint
from flask import request, jsonify
from project.models import User
from project import db
from sqlalchemy.exc import IntegrityError


@users_blueprint.route("/")
def index():
    return "Hello World!"


@users_blueprint.route("/test")
def testMigration():
    user = User("aaa", "asdfasdf", "Yulie")
    db.session.add(user)
    db.session.commit()


# Register new user
@users_blueprint.route("/users", methods=["POST"])
def register():
    try:
        user_data = request.json

        new_user = User(
            user_data.get("email"), user_data.get("password"), user_data.get("name")
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"result": 0, "message": "success"})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"result": 1, "message": "existing user"})

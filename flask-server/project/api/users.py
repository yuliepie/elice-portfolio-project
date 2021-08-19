from . import users_blueprint
from flask import request, jsonify, current_app
from project.models import User
from project import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user


@users_blueprint.route("/")
def index():
    return jsonify({"result": "success"})


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
        return jsonify({"result": 1, "message": "registration success"})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"result": 0, "message": "existing user"})
    except:
        db.session.rollback()
        return jsonify({"result": 0, "message": "registration fail"})


# Login user
@users_blueprint.route("/login", methods=["POST"])
def login():
    # Check already logged in
    if current_user.is_authenticated:
        current_app.logger.info(
            f"Duplicate login attempt by user: {current_user.email}"
        )
        return jsonify({"result": 0, "meesage": "already logged in."})

    login_data = request.json
    user = User.query.filter_by(email=login_data.get("email")).first()
    if user and user.is_password_correct(login_data.get("password")):
        # valid credentials - log in user
        login_user(user, remember=True)
        current_app.logger.info(f"Logged in user: {current_user.email}")
        return {"result": 1, "message": f"{current_user.email}, {current_user.name}"}

    return jsonify({"result": 0, "message": "invalid credentials"})


# Logout user
@users_blueprint.route("/logout")
@login_required
def logout():
    current_app.logger.info(f"Logged out user: {current_user.email}")
    logout_user()
    return jsonify({"result": 1, "message": "logout success"})

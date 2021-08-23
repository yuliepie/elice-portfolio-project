from . import users_blueprint
from flask import json, request, jsonify, current_app
from project.models import User
from project import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
import click


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
        return jsonify({"result": 0, "message": "already logged in."})

    login_data = request.json
    user = User.query.filter_by(email=login_data.get("email")).first()
    if user and user.is_password_correct(login_data.get("password")):
        # valid credentials - log in user
        login_user(user, remember=True)
        current_app.logger.info(f"Logged in user: {current_user.email}")
        return {
            "result": 1,
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name,
            },
            "message": "login success",
        }

    return jsonify({"result": 0, "message": "invalid credentials"}), 401


# Logout user
@users_blueprint.route("/logout")
@login_required
def logout():
    current_app.logger.info(f"Logged out user: {current_user.email}")
    logout_user()
    return jsonify({"result": 1, "message": "logout success"})


# View all users
@users_blueprint.route("/users")
def view_users():
    search_query = request.args.get("name", type=str)
    if search_query:
        print(search_query)
        users = db.session.query(User.id, User.name, User.description).filter(
            User.name.like(search_query + "%")
        )
    else:
        users = db.session.query(User.id, User.name, User.description).all()

    result = [dict(user) for user in users]
    return jsonify(
        {
            "result": 1,
            "users": result,
        }
    )


@users_blueprint.route("/whoami")
def check_current_user():
    if current_user.is_authenticated:
        return jsonify(
            {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name,
            }
        )


######################
#### cli commands ####
######################

# flask users create_default_users
@users_blueprint.cli.command("create_default_users")
def create_default_users():
    """Create three new users and add them to the database"""
    user1 = User("john@app.com", "12341234", "김존수")
    user1.description = "안녕하세요 김존수입니다!!!"
    user2 = User("sally@app.com", "12341234", "김샐리")
    user2.description = "안녕하세요 김샐리입니다!!!"
    user3 = User("peter@app.com", "12341234", "박피터")
    user3.description = "안녕하세요 박피터입니다!!!"
    db.session.add_all([user1, user2, user3])
    db.session.commit()


@users_blueprint.cli.command("delete_users")
def delete_users():
    """Clear all user records from table."""
    db.session.query(User).delete()
    db.session.commit()


@users_blueprint.cli.command("create_user")
@click.argument("email")
@click.argument("pw")
@click.argument("name")
@click.argument("desc")
def create(email, pw, name, desc):
    """Create a new user and add it to the database"""
    user = User(email, pw, name)
    user.description = desc
    db.session.add(user)
    db.session.commit()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import logging
from flask.logging import default_handler


#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions in the global scope.
# To be initialized with Flask App.
db = SQLAlchemy()
db_migration = Migrate()
bcrypt = Bcrypt()
login = LoginManager()


######################################
#### Application Factory Function ####
######################################

"""
An application factory function needs to:
- Create the Flask application as an instance of the Flask class
- Set configuration variables
- Register the blueprints
- Configure the logger
"""


def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)

    return app


def register_blueprints(app):
    # Import & register blueprints
    from project.api import users_blueprint
    from project.api import user_details_blueprint

    app.register_blueprint(users_blueprint, url_prefix="/api")
    app.register_blueprint(user_details_blueprint, url_prefix="/api")


def initialize_extensions(app):
    db.init_app(app)
    db_migration.init_app(app, db)
    bcrypt.init_app(app)
    login.init_app(app)

    # flask-login configuration - loads user object from session
    from project.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def configure_logging(app):
    # Logging Configuration
    file_handler = RotatingFileHandler(
        "instance/elice-portfolio-app.log", maxBytes=16384, backupCount=20  # UPDATED!
    )
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info("Starting the Flask Elice Portfolio App...")

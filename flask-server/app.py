from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from db_connect import db  # import SQLAlchemy object
from api.user import users_blueprint

# Extensions to initialize with app
db_migration = Migrate()
bcrypt = Bcrypt()

# Create a Flask instance
app = Flask(__name__)
app.register_blueprint(users_blueprint)

# Configs
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:root@localhost/elice_portfolio_db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "BLKJSSLDIJLJFLKSJDFLIJ"

# Initializations
db.init_app(app)
db_migration.init_app(app, db)
bcrypt.init_app(app)

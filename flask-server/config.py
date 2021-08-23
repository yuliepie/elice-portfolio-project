import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="asdfasdfasdf")

    # Configure Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", default="mysql+pymysql://root:root@localhost/elice_portfolio_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI",
        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}",
    )
    BCRYPT_LOG_ROUNDS = 4

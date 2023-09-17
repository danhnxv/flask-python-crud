import os


class AppConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ENGINE_OPTIONS = dict(expire_on_commit=False)
    SERVER_NAME = os.getenv("SERVER_NAME")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class DevelopmentConfig(AppConfig):
    DEBUG = True


class TestingConfig(AppConfig):
    TESTING = True

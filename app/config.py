class AppConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = dict(expire_on_commit=False)
    SERVER_NAME = "localhost:5000"


class DevelopmentConfig(AppConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://danhnv:123456@localhost:5432/todo"


class TestingConfig(AppConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://danhnv:123456@localhost:5432/todo_test"

import os
from flask import Flask
from flask_cors import CORS, cross_origin


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='simple_todo_app'
    )

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)

    @app.route('/')
    @cross_origin()
    def test():
        return 'API is up and running'

    from . import api
    app.register_blueprint(api.bp)

    from . import db
    db.init_app(app)

    return app

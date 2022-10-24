import os

import pytest

from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from pytodo import create_app
from pytodo.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DB_NAME': 'simple_todo_app_test'
    })

    with app.app_context():
        init_db()
        db = get_db()
        cur = db.cursor()
        cur.execute(_data_sql)
        db.commit()

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()

from flask import Flask
from flask.testing import FlaskClient

from pytodo.db import get_db


def test_get_users_tasks_ok(client: FlaskClient):
    response = client.get('/api/users/1/tasks')
    assert response.status_code == 200
    assert response.json == [
        {
            'id': 1,
            'title': 'Test task 1',
            'isCompleted': False
        },
        {
            'id': 2,
            'title': 'Test task 2',
            'isCompleted': True
        }
    ]


def test_get_users_tasks_not_found(client: FlaskClient):
    response = client.get('/api/users/20/tasks')
    assert response.status_code == 404
    assert bool(response.json)
    if response.json:
        assert response.json['message'] == "Couldn't find user"

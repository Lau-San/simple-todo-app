from flask import Flask
from flask.testing import FlaskClient
from pytodo.db import get_db


def test_get_all_users(client: FlaskClient, app: Flask):
    response = client.get('/api/users/')

    assert response.status_code == 200
    assert response.json == [
        {
            'id': 1,
            'username': 'test',
            'password': '$2b$10$5ysgXZUJi7MkJWhEhFcZTObGe18G1G.0rnXkewEtXq6ebVx1qpjYW'
        },
        {
            'id': 2,
            'username': 'other',
            'password': '$2b$10$Wdj1lOudt3JXEc6TBI2C6.Wafuv33FRdv9jRd9qtVdPYWmKmbtiTm'
        }
    ]


def test_get_user_by_id_ok(client: FlaskClient):
    response = client.get('/api/users/1')
    assert response.status_code == 200
    assert response.json == {
        'id': 1,
        'username': 'test',
        'password': '$2b$10$5ysgXZUJi7MkJWhEhFcZTObGe18G1G.0rnXkewEtXq6ebVx1qpjYW'
    }


def test_get_user_by_id_not_found(client: FlaskClient):
    assert client.get('/api/users/20').status_code == 404

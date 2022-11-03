from flask import Flask
from flask.testing import FlaskClient
from pytodo.db import get_db


def test_add_user_ok(client: FlaskClient, app: Flask):
    assert client.post(
        '/api/users/new',
        json={'username': 'New User', 'password': 'Some password'}
    ).status_code == 200

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            'SELECT * FROM users WHERE username = %s',
            ('New User',)
        )
        search = cur.fetchall()
        assert search


def test_add_user_wrong_content_type(client: FlaskClient):
    response = client.post('/api/users/new')

    assert response.status_code == 400
    assert response.json is not None
    assert response.json['message'] == \
        'Wrong content type. Expected application/json'


def test_add_user_no_data(client: FlaskClient, app: Flask):
    response = client.post(
        '/api/users/new',
        json={}
    )

    assert response.status_code == 400
    assert response.json is not None
    assert response.json['message'] == 'No user data to add'


def test_add_user_no_username(client: FlaskClient):
    response = client.post(
        '/api/users/new',
        json={'username': 'no password'}
    )

    assert response.status_code == 400
    assert response.json is not None
    assert response.json['message'] == 'No password was provided for new user'


def test_add_user_no_password(client: FlaskClient):
    response = client.post(
        '/api/users/new',
        json={'password': 'Don\'t add me'}
    )

    assert response.status_code == 400
    assert response.json is not None
    assert response.json['message'] == 'No username was provided for new user'


def test_add_user_already_exists(client: FlaskClient):
    response = client.post(
        '/api/users/new',
        json={
            'username': 'test',
            'password': 'Already exists'
        }
    )

    assert response.status_code == 404
    assert response.json is not None
    assert response.json['message'] == 'User already exists'

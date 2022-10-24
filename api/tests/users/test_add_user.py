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


def test_add_user_incomplete_data(client: FlaskClient, app: Flask):
    # No password

    response = client.post(
        '/api/users/new',
        json={'username': 'no password'}
    )
    assert response.status_code == 400

    if response.json:
        assert 'Not enough' in response.json['message']

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            'SELECT * FROM users WHERE username = %s',
            ('no password',)
        )
        search = cur.fetchall()
        assert not search

    # No username

    response = client.post(
        '/api/users/new',
        json={'password': 'Don\'t add me'}
    )
    assert response.status_code == 400

    if response.json:
        assert 'Not enough' in response.json['message']

    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            'SELECT * FROM users WHERE password = %s',
            ('Don\'t add me',)
        )
        search = cur.fetchall()
        assert not search


def test_add_user_no_data(client: FlaskClient, app: Flask):
    response = client.post(
        '/api/users/new',
        json={}
    )
    assert response.status_code == 400

    if response.json:
        assert 'No user' in response.json['message']

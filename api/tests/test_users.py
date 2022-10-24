from flask import Flask
from flask.testing import FlaskClient
from pytodo.db import get_db


def test_get_users(client: FlaskClient, app: Flask):
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


def test_add_user(client: FlaskClient, app: Flask):
    def search_user_by_username(username: str):
        with app.app_context():
            db = get_db()
            cur = db.cursor()
            cur.execute(
                'SELECT * FROM users WHERE username = %s',
                (username,)
            )
            search = cur.fetchall()
            return search

    # Add a user successfully
    assert client.post(
        '/api/users/new',
        json={'username': 'New User', 'password': 'Some password'}
    ).status_code == 200
    assert search_user_by_username('New User')

    # Incomplete data

    # No password
    response = client.post(
        '/api/users/new',
        json={'username': 'no password'}
    )
    assert response.status_code == 400
    if response.json:
        assert 'Not enough' in response.json['message']
    assert not search_user_by_username('no password')

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

    # No data
    response = client.post(
        '/api/users/new',
        json={}
    )
    assert response.status_code == 400
    if response.json:
        assert 'No user' in response.json['message']

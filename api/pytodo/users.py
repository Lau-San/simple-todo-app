from typing import Union, Any
from flask import Blueprint, jsonify, request, make_response
from .db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=('GET',))
def get_all_users():
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users;')
        result = cur.fetchall()

    response = []
    for _, user_data in enumerate(result):
        response.append({
            'id': user_data[0],
            'username': user_data[1],
            'password': user_data[2]
        })

    response = jsonify(response)
    response.status_code = 200
    return response


@bp.route('/new', methods=('POST',))
def add_user():
    response = make_response()

    # Get json data from request
    data = request.get_json()

    # Check that data is not empty
    if not data:
        response = jsonify({
            'message': 'No user data'
        })
        response.status_code = 400
        return response

    # Check that data has username and password
    try:
        username = data['username']
        password = data['password']
    except KeyError:
        response = jsonify({
            'message': 'Not enough user data',
        })
        response.status_code = 400
        return response

    db = get_db()
    with db.cursor() as cur:

        # Check if user is already in database
        cur.execute('SELECT id FROM users WHERE username = %s', (username,))
        result = cur.fetchall()
        if result:
            response = jsonify({
                'message': 'User already exists',
            })
            response.status_code = 400
            return response

        # Add new user
        cur.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            (username, password)
        )
        db.commit()

    return response


@bp.route('/<int:user_id>')
def get_user_by_id(user_id: int):
    exists, user = get_user_data(user_id)

    if not exists:
        response = jsonify({
            'message': "User doesn't exist"
        })
        response.status_code = 404
        return response

    response = jsonify(user)
    return response


def get_user_data(id: int) -> tuple[bool, Union[dict[str, Any], Any]]:
    """Retrieve the user with the given id if it exists."""

    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE id = %s', (id,))
        search = cur.fetchone()

    if not search:
        return (False, None)

    user = {
        'id': search[0],
        'username': search[1],
        'password': search[2]
    }

    return (True, user)

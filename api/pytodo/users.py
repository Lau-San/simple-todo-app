from typing import Union, Any
from flask import Blueprint, jsonify, request, make_response
from .db import get_db
from .utils import get_user_data, query_result_to_tasks

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=('GET',))
def get_all_users():
    """Get a list of all users."""

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
    """Add a new user to the database."""

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


@bp.route('/<int:user_id>', methods=('GET',))
def get_user(user_id: int):
    user_exists, user = get_user_data(user_id)

    if not user_exists:
        response = jsonify({
            'message': "User doesn't exist"
        })
        response.status_code = 404
        return response

    response = jsonify(user)
    return response


@bp.route('/<int:user_id>/tasks', methods=('GET',))
def get_user_tasks(user_id: int):
    user_exists, _ = get_user_data(user_id)

    if not user_exists:
        response = jsonify({
            'message': "User doesn't exist"
        })
        response.status_code = 404
        return response

    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks WHERE user_id = %s', (user_id,))
        search = cur.fetchall()

    tasks = query_result_to_tasks(search)
    response = jsonify(tasks)
    return response

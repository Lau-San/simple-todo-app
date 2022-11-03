from typing import Union, Any
from flask import Blueprint, jsonify, request, make_response
from psycopg2.errors import UniqueViolation
from .db import get_db
from .utils import get_user_data, query_result_to_tasks, new_error_response

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=('GET',))
def get_all_users():
    """Get a list of all users."""

    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users;')
        search = cur.fetchall()

    users = []
    for _, user_data in enumerate(search):
        users.append({
            'id': user_data[0],
            'username': user_data[1],
            'password': user_data[2]
        })

    return jsonify(users)


@bp.route('/new', methods=('POST',))
def add_user():
    """Add a new user to the database."""

    # Check that data type is correct
    if request.content_type != 'application/json':
        return new_error_response(
            400,
            'Wrong content type. Expected application/json'
        )

    # Get json data from request
    new_user_data = request.get_json()

    # Check that data is not empty
    if not new_user_data:
        return new_error_response(400, 'No user data to add')

    # Check that data has username and password
    if 'username' not in new_user_data:
        return new_error_response(400, 'No username was provided for new user')
    if 'password' not in new_user_data:
        return new_error_response(400, 'No password was provided for new user')

    db = get_db()
    with db.cursor() as cur:
        try:
            cur.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (new_user_data['username'], new_user_data['password'])
            )
        except UniqueViolation:
            return new_error_response(404, 'User already exists')

        db.commit()

    return make_response()


@bp.route('/<int:user_id>', methods=('GET',))
def get_user(user_id: int):
    user_exists, user = get_user_data(user_id)

    if not user_exists:
        return new_error_response(404, "User doesn't exist")

    return jsonify(user)


@bp.route('/<int:user_id>/tasks', methods=('GET',))
def get_user_tasks(user_id: int):
    # Check if user exists
    user_exists, _ = get_user_data(user_id)
    if not user_exists:
        return new_error_response(404, "User doesn't exist")

    # Search user's tasks
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks WHERE user_id = %s', (user_id,))
        search = cur.fetchall()

    tasks = query_result_to_tasks(search)
    return jsonify(tasks)

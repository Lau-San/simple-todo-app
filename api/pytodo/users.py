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
            'message': 'Where\'s my user data?'
        })
        response.status_code = 400
        return response

    # Check that data has username and password
    try:
        username = data['username']
        password = data['password']
    except KeyError:
        response = jsonify({
            'message': 'You probably forgot to send a username or a password',
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

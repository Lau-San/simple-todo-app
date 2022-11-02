from typing import Any
from flask import jsonify, Blueprint, request, make_response
from .db import get_db
from .utils import query_result_to_tasks, new_error_response, get_user_data

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('', methods=('GET',))
def get_all_tasks():
    db = get_db()

    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks')
        search = cur.fetchall()

    tasks = query_result_to_tasks(search)
    return jsonify(tasks)


@bp.route('/new', methods=('POST',))
def add_task():
    # Check that data type is correct
    if request.content_type != 'application/json':
        return new_error_response(
            400,
            'Wrong content type. Expected application/json'
        )

    # Check that data exists or is not empty
    try:
        new_task_data: Any
        new_task_data = request.get_json()
    except Exception:
        return new_error_response(400, 'No task data to add')

    # Check that all needed data was provided
    for prop in ['title', 'userId']:
        if prop not in new_task_data:
            return new_error_response(
                400,
                f'No {prop} was provided for the new task'
            )

    # Check that user exists
    user_exists, _ = get_user_data(new_task_data['userId'])
    if not user_exists:
        return new_error_response(404, "User doesn't exist")

    # Add the task
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            'INSERT INTO tasks (user_id, title) VALUES (%s, %s)',
            (new_task_data['userId'], new_task_data['title'])
        )
        db.commit()

    return make_response()

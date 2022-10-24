from typing import Any
from flask import jsonify, Blueprint, request
from .users import get_user_data
from .db import get_db

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/', methods=('GET',))
def get_all_users_tasks():
    db = get_db()
    data = request.get_json()

    if not data:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM tasks')
            search = cur.fetchall()
        tasks = query_res_to_task_list(search)
        response = jsonify(tasks)
        return response

    user_exists, user = get_user_data(data['userId'])

    if not user_exists:
        response = jsonify({
            'message': "Couldn't find user"
        })
        response.status_code = 404
        return response

    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks WHERE user_id = %s', (user['id'],))
        search = cur.fetchall()

    tasks = query_res_to_task_list(search)
    response = jsonify(tasks)
    return response


def query_res_to_task_list(res: list[tuple]) -> list[dict[str, Any]]:
    tasks = []
    for result in res:
        tasks.append({
            'id': result[0],
            'userId': result[1],
            'title': result[2],
            'isCompleted': result[3]
        })
    return tasks

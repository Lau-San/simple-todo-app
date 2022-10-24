from flask import jsonify
from .users import bp, get_user_data
from .db import get_db


@bp.route('/<int:user_id>/tasks')
def get_all_users_tasks(user_id: int):
    exists, user = get_user_data(user_id)

    if not exists:
        response = jsonify({
            'message': "Couldn't find user"
        })
        response.status_code = 404
        return response

    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks WHERE user_id = %s', (user['id'],))
        search = cur.fetchall()

    tasks = []
    for result in search:
        tasks.append({
            'id': result[0],
            'user_id': result[1],
            'title': result[2],
            'isCompleted': result[3]
        })

    response = jsonify(tasks)
    return response

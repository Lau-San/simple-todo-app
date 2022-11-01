from typing import Any
from flask import jsonify, Blueprint
from .db import get_db
from .utils import query_result_to_tasks

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('', methods=('GET',))
def get_all_tasks():
    db = get_db()

    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks')
        search = cur.fetchall()

    tasks = query_result_to_tasks(search)
    response = jsonify(tasks)
    return response

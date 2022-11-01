from typing import Union, Any
from .db import get_db


def query_result_to_tasks(res: list[tuple]) -> list[dict[str, Any]]:
    """
    Format the given query result and return it as a more usable list of 
    dictionaries
    """

    tasks = []
    for result in res:
        tasks.append({
            'id': result[0],
            'userId': result[1],
            'title': result[2],
            'isCompleted': result[3]
        })
    return tasks


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

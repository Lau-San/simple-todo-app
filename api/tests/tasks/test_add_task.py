from flask.testing import FlaskClient
from pytodo.db import get_db
from pytodo.utils import query_result_to_tasks


def test_add_task_ok(client: FlaskClient):
    task = {
        'id': 4,
        'userId': 2,
        'title': 'New test task',
        'isCompleted': False
    }

    response = client.post(
        '/api/tasks/new',
        json={
            'userId': task['userId'],
            'title': task['title']
            # 'isCompleted': False
        }
    )

    assert response.status_code == 200

    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks')
        search = cur.fetchall()

    tasks = query_result_to_tasks(search)
    # Check that the new task is in the list
    assert task in tasks


def test_add_task_no_title(client: FlaskClient):
    response = client.post(
        '/api/tasks/new',
        json={
            'userId': 2
        }
    )

    assert response.status_code == 400
    assert response.json is not None
    assert response.json['message'] == 'Title is required'

    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks WHERE user_id = 2')
        search = cur.fetchall()

    tasks = query_result_to_tasks(search)

    assert len(tasks) == 1

    # Check that the only task in the result is the task that was already in
    # the database (no task has been added)
    assert tasks[0] == {
        'id': 3,
        'userId': 2,
        'title': 'Another test task',
        'isCompleted': False
    }


def test_add_task_no_user_id(client: FlaskClient):
    response = client.post(
        '/api/tasks/new',
        json={
            'title': 'New test task'
        }
    )

    assert response.status_code == 400
    assert response.json is not None
    assert response.json['message'] == "User id is required"

    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks')
        search = cur.fetchall()

    tasks = query_result_to_tasks(search)

    assert len(tasks) == 1

    # Check that the only task in the result is the task that was already in
    # the database (no task has been added)
    assert tasks[0] == {
        'id': 3,
        'userId': 2,
        'title': 'Another test task',
        'isCompleted': False
    }


def test_add_task_user_doesnt_exist(client: FlaskClient):
    task = {
        'id': 4,
        'userId': 20,
        'title': 'New test task',
        'isCompleted': False
    }

    response = client.post(
        '/api/tasks/new',
        json={
            'userId': task['userId'],
            'title': task['title']
            # 'isCompleted': False
        }
    )

    assert response.status_code == 404
    assert response.json is not None
    assert response.json['message'] == "User doesn't exist"

    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM tasks WHERE user_id = 20')
        search = cur.fetchall()

    tasks = query_result_to_tasks(search)

    assert not tasks

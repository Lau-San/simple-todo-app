from flask.testing import FlaskClient
from werkzeug.wrappers import response


def test_get_all_tasks(client: FlaskClient):
    response = client.get(
        '/api/tasks/',
        json={}
    )

    assert response.status_code == 200
    assert response.json == [
        {
            'id': 1,
            'userId': 1,
            'title': 'Test task 1',
            'isCompleted': False
        },
        {
            'id': 2,
            'userId': 1,
            'title': 'Test task 2',
            'isCompleted': True
        },
        {
            'id': 3,
            'userId': 2,
            'title': 'Another test task',
            'isCompleted': False
        }
    ]


def test_get_users_tasks_ok(client: FlaskClient):
    response = client.get(
        '/api/tasks/',
        json={'userId': 1}
    )
    assert response.status_code == 200
    assert response.json == [
        {
            'id': 1,
            'userId': 1,
            'title': 'Test task 1',
            'isCompleted': False
        },
        {
            'id': 2,
            'userId': 1,
            'title': 'Test task 2',
            'isCompleted': True
        }
    ]


def test_get_users_tasks_not_found(client: FlaskClient):
    response = client.get(
        '/api/tasks/',
        json={'userId': 20}
    )
    assert response.status_code == 404

    assert response.json is not None
    assert response.json['message'] == "Couldn't find user"

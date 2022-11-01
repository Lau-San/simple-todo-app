from flask.testing import FlaskClient
from werkzeug.wrappers import response


def test_get_all_tasks(client: FlaskClient):
    response = client.get(
        '/api/tasks',
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

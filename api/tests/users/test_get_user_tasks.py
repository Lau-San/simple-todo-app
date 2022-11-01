from flask.testing import FlaskClient


def test_get_users_tasks_ok(client: FlaskClient):
    response = client.get('/api/users/1/tasks')

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
    response = client.get('/api/users/20/tasks')
    assert response.status_code == 404

    assert response.json is not None
    assert response.json['message'] == "User doesn't exist"

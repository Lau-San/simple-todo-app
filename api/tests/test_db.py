import pytest
from pytest import MonkeyPatch
import psycopg2
from flask import Flask
from flask.testing import FlaskCliRunner

from pytodo.db import get_db


def test_get_close_db(app: Flask):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(psycopg2.InterfaceError) as e:
        cur = db.cursor()
        cur.execute('SELECT 1;')

    assert 'closed' in str(e.value)


def test_init_db_command(runner: FlaskCliRunner, monkeypatch: MonkeyPatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('pytodo.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

import os
import click
import psycopg2
from psycopg2.extras import DictCursor
from flask import g, current_app, Flask


def get_db():
    if 'db' not in g:
        print(os.getenv('DB_URL'))
        if os.getenv('DB_URL'):
            g.db = psycopg2.connect(
                os.getenv('DB_URL'),
                # sslmode='require',
                cursor_factory=DictCursor,
            )
        else:
            g.db = psycopg2.connect(
                cursor_factory=DictCursor,
                host=os.getenv('DB_HOST'),
                dbname=current_app.config['DB_NAME'],
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db:
        db.close()


def init_db():
    db = get_db()
    cur = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        cur.execute(f.read().decode('utf8'))
        db.commit()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized database')


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

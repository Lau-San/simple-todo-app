from flask import Blueprint
from . import users, tasks

bp = Blueprint('api', __name__, url_prefix='/api')
bp.register_blueprint(users.bp)
bp.register_blueprint(tasks.bp)


@bp.route('/', methods=('GET',))
def api():
    return 'Api test'

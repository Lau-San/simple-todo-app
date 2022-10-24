from flask import Blueprint
# skipcq PY-W2000
from . import users, tasks

bp = Blueprint('api', __name__, url_prefix='/api')
bp.register_blueprint(users.bp)


@bp.route('/', methods=('GET',))
def api():
    return 'Api test'

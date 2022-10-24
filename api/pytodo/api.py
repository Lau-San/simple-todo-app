from flask import Blueprint
from . import users

bp = Blueprint('api', __name__, url_prefix='/api')
bp.register_blueprint(users.bp)


@bp.route('/', methods=('GET',))
def api():
    return 'Api test'

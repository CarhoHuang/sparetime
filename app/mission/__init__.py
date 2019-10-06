from flask import Blueprint

bp = Blueprint('missions', __name__, url_prefix='/missions')
from . import missions
from . import mission_comments

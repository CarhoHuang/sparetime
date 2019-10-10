from flask import Blueprint

bp = Blueprint('mission', __name__, url_prefix='/mission')
from . import missions
from . import mission_comments

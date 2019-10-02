from flask import Blueprint

bp = Blueprint('idle_thing', __name__, url_prefix='/idle_thing')
from . import idle_thing
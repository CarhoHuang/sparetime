from flask import Blueprint

bp = Blueprint('search_thing', __name__, url_prefix='/search_thing')
from . import search_thing
from . import search_thing_comment

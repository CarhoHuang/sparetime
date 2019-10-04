from flask import Blueprint

bp = Blueprint('mission', __name__, url_prefix='/mission')
from . import mission
from . import comment

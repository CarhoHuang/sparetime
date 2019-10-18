from flask import Blueprint

bp = Blueprint('study', __name__, url_prefix='/study')
from . import study
from . import study_comment

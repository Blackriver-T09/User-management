# admin_api/__init__.py
from flask import Blueprint

admin_api = Blueprint('admin_api', __name__)

from .admin_dashboard import *
from .other_admin_apis import *

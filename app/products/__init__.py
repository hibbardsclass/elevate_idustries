from flask import Blueprint

# Ensure the template folder path is correctly referenced relative to the blueprint
products = Blueprint('products', __name__,
                     template_folder='templates', static_folder='static')

from . import routes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure logging
    if app.config['DEBUG']:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # This will be the endpoint for your login page

    # Initialize Flask-Principal
    principals = Principal(app)

    # Define Permissions
    admin_permission = Permission(RoleNeed('admin'))
    seller_permission = Permission(RoleNeed('seller'))
    customer_permission = Permission(RoleNeed('customer'))

    # Initialize Flask-Admin
    from app.models import User, Product, Role, Order, OrderItem
    admin = Admin(app, name='Elevate Industries Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(OrderItem, db.session))


    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.products import products as products_blueprint
    app.register_blueprint(products_blueprint, url_prefix='/products')

    from app.orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint, url_prefix='/orders')

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # User loader function setup for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(user_id)

    return app

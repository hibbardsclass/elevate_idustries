from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed, identity_changed, Identity, identity_loaded, UserNeed
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
    app.admin_permission = Permission(RoleNeed('admin'))
    app.seller_permission = Permission(RoleNeed('seller'))
    app.customer_permission = Permission(RoleNeed('customer'))

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
        user = User.query.get(user_id)
        if user:
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            print(f'User {user.username} logged in with role {user.role.name}')  # Add debug print
        return user

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        user = User.query.get(identity.id)
        identity.user = user

        if user:
            identity.provides.add(UserNeed(user.id))
            if user.role:
                identity.provides.add(RoleNeed(user.role.name))
                print(f'Loaded identity for user {user.username} with role {user.role.name}')  # Add debug print

    # Register CLI commands
    from app.commands import init_roles_command, create_admin_user_command
    app.cli.add_command(init_roles_command)
    app.cli.add_command(create_admin_user_command)

    return app

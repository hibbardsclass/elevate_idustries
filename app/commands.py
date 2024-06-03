from app import db
from app.models import User, Role
from flask.cli import with_appcontext
import click

@click.command(name='init_roles')
@with_appcontext
def init_roles_command():
    roles = ['admin', 'seller', 'customer']
    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()
    print("Roles initialized")

@click.command(name='create_admin_user')
@with_appcontext
def create_admin_user_command():
    role = Role.query.filter_by(name='admin').first()
    if role:
        admin_user = User(username='admin', email='rhibbard@elevate208.org', role_id=role.id)
        admin_user.set_password('hibbardsclass23')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created")

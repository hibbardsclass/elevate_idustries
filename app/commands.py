from app import db
from app.models import User, Role

def init_roles():
    roles = ['admin', 'seller', 'customer']
    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()

def create_admin_user():
    role = Role.query.filter_by(name='admin').first()
    if role:
        admin_user = User(username='admin', email='rhibbard@elevate208.org', role=role)
        admin_user.set_password('hibbardsclass23')
        db.session.add(admin_user)
        db.session.commit()

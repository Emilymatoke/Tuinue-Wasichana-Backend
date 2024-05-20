from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from roles import Role  # Import Role class

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), nullable=False, default=Role.DONOR)  # Adding the role column
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    donations = db.relationship('Donation', backref='user', lazy=True)

class Charity(db.Model):
    __tablename__ = 'charities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_email = db.Column(db.String(150), unique=True, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    donations = db.relationship('Donation', backref='charity', lazy=True)
    stories = db.relationship('Beneficiary', backref='charity', lazy=True)

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    recurring = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)

class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('pending', 'completed', 'failed', name='status_enum'), nullable=False)








# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Enum
# from datetime import datetime
# from flask_rbac import RoleMixin,UserMixin

# db = SQLAlchemy()


# # roles_parents = db.Table(
# #     'roles_parents',
# #     db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
# #     db.Column('parent_id', db.Integer, db.ForeignKey('role.id'))
# # )
# # users_roles = db.Table(
# #     'users_roles',
# #     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
# #     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
# # )
# roles_users = db.Table('roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )

# class User(db.Model, UserMixin):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     email = db.Column(db.String, unique=True)
#     password = db.Column(db.String(255), nullable=False, server_default='')
#     active = db.Column(db.Boolean())
#     roles = db.relationship('Role', secondary=roles_users, backref='roled')


# class Role(db.Model, RoleMixin):
#     __tablename__ = 'role'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)

# # class User(db.Model, UserMixin):
# #     __tablename__ = 'users'
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(255), nullable=False)
# #     password = db.Column(db.String(255), nullable=False)
# #     email = db.Column(db.String(255), nullable=False)
# #     parents = db.relationship(
# #         'Role',
# #         secondary=roles_parents,
# #         primaryjoin=(id == roles_parents.c.role_id),
# #         secondaryjoin=(id == roles_parents.c.parent_id),
# #         backref=db.backref('children', lazy='dynamic')
# #     )
# #     # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
# #     def add_role(self, role):
# #         self.roles.append(role)

# #     def add_roles(self, roles):
# #         for role in roles:
# #             self.add_role(role)

# #     def get_roles(self):
# #         for role in self.roles:
# #             yield role

# # class Role(db.Model, RoleMixin):
# #     __tablename__ = 'role'
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(80), unique=True)
# #     permissions=db.Column(db.PickleType)
# #     parents = db.relationship(
# #         'Role',
# #         secondary=roles_parents,
# #         primaryjoin=(id == roles_parents.c.role_id),
# #         secondaryjoin=(id == roles_parents.c.parent_id),
# #         backref=db.backref('children', lazy='dynamic')
# #     )
# #     def __init__(self, name):
# #         RoleMixin.__init__(self)
# #         self.name = name

# #     def add_parent(self, parent):
# #         self.parents.append(parent)

# #     def add_parents(self, *parents):
# #         for parent in parents:
# #             self.add_parent(parent)

# #     @staticmethod
# #     def get_by_name(name):
# #         return Role.query.filter_by(name=name).first()
    
# class Charity(db.Model):
#     __tablename__ = 'charities'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     contact_email = db.Column(db.String(150), unique=True, nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     is_approved = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationships
#     donations = db.relationship('Donation', backref='charity', lazy=True)
#     stories = db.relationship('Beneficiary', backref='charity', lazy=True)

#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description,
#             'contact_email': self.contact_email
#         }

# class Donation(db.Model):
#     __tablename__ = 'donations'
#     id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.Float, nullable=False)
#     recurring = db.Column(db.Boolean, nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     is_anonymous = db.Column(db.Boolean, default=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)

# class Beneficiary(db.Model):
#     __tablename__ = 'beneficiaries'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     posted_at = db.Column(db.DateTime, default=datetime.utcnow)
#     charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)


# def init_db(app):
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()






















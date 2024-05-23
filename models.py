from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    role = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    donations = db.relationship('Donation', backref='user', lazy=True)
    
    def __init__(self, name, email, password_hash, address, gender, role):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.address = address
        self.gender = gender
        self.role = role

    def __repr__(self):
        return f'<User {self.email}>'
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

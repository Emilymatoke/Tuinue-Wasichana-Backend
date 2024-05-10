from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    users_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    # Relationship
    donations = db.relationship('Donation', backref='user', lazy=True)

class Charity(db.Model):
    __tablename__ = 'charities'
    
    charity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_email = db.column(db.string (150), unique=True, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    donations = db.relationship('Donation', backref='charity', lazy=True)
    stories = db.relationship('Story', backref='charity', lazy=True)

class Donation(db.Model):
    __tablename__ = 'donations'
    
    donation_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    recurring = db.column(db.boolean, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)

class Story(db.Model):
    __tablename__ = 'stories'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)

    class Donation(db.Model):
     __tablename__ = 'payments'
    
    payment_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.column(db.string, nullable=False)
    transaction_id = db.Column(db.string, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('pending', 'completed', 'failed'), nullable=False)
    

# Setup for Flask-SQLAlchemy
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

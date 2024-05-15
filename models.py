from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Enum
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String,nullable = False)
    password=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    role=db.Column(Enum('donor','charity','administrator',name='role_types'),nullable=False)


class Charity(db.Model):
    __tablename__ = 'charities'
    
    charity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    donations = db.relationship('Donation', backref='charity', lazy=True)
    stories = db.relationship('Story', backref='charity', lazy=True)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'contact_email': self.contact_email
        }

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    recurring = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)

class Benaficiary(db.Model):
    __tablename__ = 'stories'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)

# class Donation(db.Model):
#             __tablename__ = 'payments'
            
#             id = db.Column(db.Integer, primary_key=True)
#             amount = db.Column(db.Float, nullable=False)
#             payment_method = db.column(db.string, nullable=False)
#             transaction_id = db.Column(db.string, nullable=False)
#             date = db.Column(db.DateTime, default=datetime.utcnow)
#             status = db.Column(db.Enum('pending', 'completed', 'failed'), nullable=False)          
        

# Setup for Flask-SQLAlchemy
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
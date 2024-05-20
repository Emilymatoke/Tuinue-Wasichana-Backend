from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app  # Assuming 'app' is your Flask application instance
from models import User, Role, Charity, Donation, Beneficiary  # Import your SQLAlchemy models

db = SQLAlchemy(app)  # Initialize SQLAlchemy with your Flask app
@app.before_request
def seed_data():
    # Create all database tables if they do not exist
    with app.app_context():
        db.create_all()

        # Create roles
        role_admin = Role(name='administrator')
        role_donor = Role(name='donor')
        role_charity = Role(name='charity')

        # Add roles to session
        db.session.add_all([role_admin, role_donor, role_charity])
        db.session.commit()

        # Create users
        user_admin = User(username='admin', password='admin123', email='admin@example.com')
        user_donor = User(username='donor1', password='donor123', email='donor@example.com')
        user_charity = User(username='charity1', password='charity123', email='charity@example.com')

        # Assign roles to users
        user_admin.add_role(role_admin)
        user_donor.add_role(role_donor)
        user_charity.add_role(role_charity)

        # Add users to session
        db.session.add_all([user_admin, user_donor, user_charity])
        db.session.commit()

        # Create charities
        charity1 = Charity(name='Charity One', contact_email='charity1@example.com', description='Description of Charity One', is_approved=True, created_at=datetime.utcnow())
        charity2 = Charity(name='Charity Two', contact_email='charity2@example.com', description='Description of Charity Two', is_approved=False, created_at=datetime.utcnow())

        # Add charities to session
        db.session.add_all([charity1, charity2])
        db.session.commit()

        # Create donations
        donation1 = Donation(amount=100.0, recurring=True, date=datetime.utcnow(), is_anonymous=False, user_id=user_donor.id, charity_id=charity1.id)
        donation2 = Donation(amount=50.0, recurring=False, date=datetime.utcnow(), is_anonymous=True, user_id=user_donor.id, charity_id=charity2.id)

        # Add donations to session
        db.session.add_all([donation1, donation2])
        db.session.commit()

        # Create beneficiaries (stories)
        beneficiary1 = Beneficiary(title='Story One', content='Story content for Charity One', posted_at=datetime.utcnow(), charity_id=charity1.id)
        beneficiary2 = Beneficiary(title='Story Two', content='Story content for Charity Two', posted_at=datetime.utcnow(), charity_id=charity2.id)

        # Add beneficiaries to session
        db.session.add_all([beneficiary1, beneficiary2])
        db.session.commit()

if __name__ == '__main__':
    seed_data()

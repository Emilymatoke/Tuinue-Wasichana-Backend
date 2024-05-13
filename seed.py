from model import db, User, Charity, Donation, Story
from datetime import datetime

def seed_data():
    # Creating users
    user1 = User(username='Alice', email='alice@example.com', password_hash='password123')
    user2 = User(username='Bob', email='bob@example.com', password_hash='password456')
    db.session.add_all([user1, user2])
    
    # Creating charities
    charity1 = Charity(name='EmpowerGirls', description='Empowering girls in marginalized areas by providing sanitary towels and water.', contact_email='contact@empowergirls.org')
    charity2 = Charity(name='GirlsAid', description='GirlsAid focuses on providing sanitary towels to girls in need.', contact_email='info@girlsaid.org')
    db.session.add_all([charity1, charity2])
    
    # Creating donations
    donation1 = Donation(amount=50.0, recurring=True, date=datetime.utcnow(), user=user1, charity=charity1)
    donation2 = Donation(amount=100.0, recurring=False, date=datetime.utcnow(), user=user2, charity=charity2)
    db.session.add_all([donation1, donation2])
    
    # Creating stories
    story1 = Story(title='EmpowerGirls Story', content='Story of empowerment through hygiene education and access to sanitary towels.', posted_at=datetime.utcnow(), charity=charity1)
    story2 = Story(title='GirlsAid Story', content='GirlsAid\'s journey in supporting girls with essential needs in marginalized areas.', posted_at=datetime.utcnow(), charity=charity2)
    db.session.add_all([story1, story2])

    # Committing changes to the database
    db.session.commit()
    print("Data seeded successfully!")

if __name__ == '__main__':
    from model import app, init_db
    init_db(app)
    seed_data()

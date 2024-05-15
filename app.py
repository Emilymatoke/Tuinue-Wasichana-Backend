from werkzeug.security import check_password_hash
from flask import Flask,request,flash,redirect,url_for,jsonify,make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import User,Charity,Donation,Benaficiary
from flask_restful import Api,Resource
from flask_rbac import RBAC,Role

app = Flask(__name__)
rbac = RBAC(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api=Api(app)
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
ROLE_DONOR='donor'
ROLE_ADMINISTRATOR='administrator'
ROLE_CHARITY='charity'
permissions_donor = [
    'view_charities',
    'choose_charity',
    'make_donation',
    'view_beneficiaries',
    'donate_via_payment'
]

permissions_charity = [
    'apply_to_be_charity',
    'view_non_anonymous_donors',
    'view_anonymous_donors',
    'view_total_donations',
    'create_beneficiary_stories',
    'manage_beneficiaries_inventory'
]
permissions_administrator = [
    'receive_charity_applications',
    'review_charity_applications',
    'approve_charity_application',
    'reject_charity_application',
    'delete_charity'
]

roles = {
    ROLE_DONOR: Role(ROLE_DONOR, permissions=permissions_donor),
    ROLE_CHARITY: Role(ROLE_CHARITY,Permissions=permissions_charity),
    ROLE_ADMINISTRATOR: Role(ROLE_ADMINISTRATOR,Permissions=permissions_administrator)
}

@app.route('/api/login')
def login(email):
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401
    else:
        flash('Login successful')
        return redirect(url_for('home'))
    # Authenticate user and set session or token
    # For simplicity, let's assume session-based authentication
    # You might want to use Flask-Login or JWT for token-based auth
    # session['user_id'] = user.id
    
@app.route('/api/charities', methods=['GET'])
@rbac.allow(['view_charities'])
def view_charities(name):
    charities = Charity.query.filter_by(name=name).first()
    return jsonify(charities.serialize())

@app.route('/api/charities/choose_charity', methods=['POST'])
@rbac.allow(['choose_charity'])
def choose_charity():
    
    flash('Charity chosen successfully')
    return redirect(url_for('donate'))

@app.route('/api/donate', methods=['POST'])
@rbac.allow(['make_donation'])
def make_donation():
    
    return jsonify({'message': 'Donation successful'})
          # Charity
@app.route('/api/apply_charity', methods=['POST'])
@rbac.allow(['apply_to_be_charity'])
def apply_charity():
    # Logic to handle charity application
    # Example: Save charity details in database
    data = request.json
    name=data.get('name')
    description=data.get('description')
    contact_email=data.get('contact_email')
    new_charity=Charity(name=name,description=description,contact_email=contact_email)

    db.session.add(new_charity)
    db.session.commit()
    return jsonify({'message': 'Charity application submitted successfully'})

@app.route('/api/non_anonymous_donors', methods=['GET'])
@rbac.allow(['view_non_anonymous_donors'])
def view_non_anonymous_donors():
    # Logic to retrieve and return non-anonymous donors and their donations
    # Example: Query the database for non-anonymous donors
    donors = Donation.query.filter_by(is_anonymous=False).all()
    donor_data = [{'donor_name': donor.donor.name, 'amount_donated': donor.amount} for donor in donors]
    return jsonify({'non_anonymous_donors': donor_data})

@app.route('/api/total_donations', methods=['GET'])
@rbac.allow(['view_total_donations'])
def view_total_donations():
    # Logic to calculate and return the total amount donated to the charity
    # Example: Query the database to sum up donations
    total_donations = sum(donation.amount for donation in Donation.query.filter_by(charity_id=Donation.id).all())
    return jsonify({'total_donations': total_donations})

@app.route('/api/create_beneficiary_story', methods=['POST'])
@rbac.allow(['create_beneficiary_stories'])
def create_beneficiary_story():
    # Logic to create and post stories of beneficiaries
    data = request.json
    title=data.get('title'),
    content=data.get('content')
    new_story=Benaficiary(data=data,title=title,content=content)
    # Save the beneficiary and story in the database
    db.session.add(new_story)
    db.session.commit()
    return jsonify({'message': 'Beneficiary story posted successfully'})

@app.route('/api/manage_beneficiaries_inventory', methods=['POST'])
@rbac.allow(['manage_beneficiaries_inventory'])
def manage_beneficiaries_inventory():
    # Logic to manage beneficiaries and inventory
    data = request.json
    beneficiary = Benaficiary.query.get(data['beneficiary_id'])
    if not beneficiary:
        return jsonify({'message': 'Beneficiary not found'}), 404
    beneficiary.inventory_sent = data['inventory_sent']
    # Update beneficiary inventory in the database
    db.session.commit()
    return jsonify({'message': 'Beneficiary inventory updated successfully'})
        # ADMINISTRATOR
@app.route('/api/charity_applications', methods=['GET'])
@rbac.allow(['receive_charity_applications'])
def get_charity_applications():
    # Logic to retrieve and return list of charity applications
    charity_applications = Charity.query.filter_by(is_approved=False).all()
    return jsonify({'charity_applications': [charity.serialize() for charity in charity_applications]})

@app.route('/api/approve_charity/<int:charity_id>', methods=['POST'])
@rbac.allow(['approve_charity_application'])
def approve_charity(charity_id):
    # Logic to approve a charity application
    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify({'message': 'Charity not found'}), 404

    charity.is_approved = True
    db.session.commit()
    return jsonify({'message': 'Charity application approved successfully'})

@app.route('/api/reject_charity/<int:charity_id>', methods=['POST'])
@rbac.allow(['reject_charity_application'])
def reject_charity(charity_id):
    try:
        # Retrieve the charity record from the database
        charity = Charity.query.get(charity_id)
        
        # Check if the charity record exists
        if not charity:
            return jsonify({'message': 'Charity not found'}), 404

        # Update the is_approved status to False
        charity.is_approved = False
        db.session.commit()

        return jsonify({'message': 'Charity application rejected successfully'})
    except Exception as e:
        # Handle database or other errors
        db.session.rollback()  # Rollback changes if an error occurs
        return jsonify({'message': f'Failed to reject charity: {str(e)}'}), 500
class Register(Resource):
    def post(self):
        data = request.json

        # Retrieve data from JSON payload
        email = data.get('email')
        username = data.get('name')
        password = data.get('password')
        confirm_password = data.get('confirm_password')  # Correct field name

        # Basic input validations
        if not email or len(email) < 4:
            flash('Email must be valid and greater than 4 characters')
            return jsonify({"error": "Invalid email"}), 400

        if not username:
            flash("Username can't be empty")
            return jsonify({"error": "Username is required"}), 400

        if password != confirm_password:
            flash('Passwords do not match')
            return jsonify({"error": "Passwords do not match"}), 400

        # Check if user with the given email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 409

        # Create a new user and add to the database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Construct response
        response_dict = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }

        # Return success response with status code 201
        return jsonify(response_dict), 201
    
api.add_resource(Register,'/register')



if __name__ == '__main__':
    app.run(port=5555, debug=True)


# def reject_charity(charity_id):
#     # Logic to reject a charity application
#     charity = Charity.query.get(charity_id)
#     if not charity:
#         return jsonify({'message': 'Charity not found'}), 404

#     db.session.delete(charity)
#     db.session.commit()
#     return jsonify({'message': 'Charity application rejected and deleted successfully'})

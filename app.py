
from flask import Flask, request, jsonify,flash,redirect,url_for
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from datetime import timedelta
from models import db, User,Charity,Beneficiary,Donation
# from config import DATABASE_CONFIG  # Import the config
import secrets

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Generate a random secret key
jwt_secret_key = secrets.token_hex(32)  # Generate a 32-byte (256-bit) random key
app.config['JWT_SECRET_KEY'] = jwt_secret_key
migrate = Migrate(app, db)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return "This is a basic Flask application"

@app.route('/admin/login', methods=['POST'])
def admin_login():
    if request.content_type != 'application/json':
        return jsonify({"success": False, "message": "Content-Type must be application/json"}), 415

    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data"}), 400
    
    # Check login credentials
    if data['email'] == 'admin@gmail.com' and data['password'] == 'password':
        expiration_time = timedelta(hours=1)
        token = create_access_token(identity='admin', expires_delta=expiration_time)
        return jsonify({"success": True, "message": "Login successful", "token": token, 'user_email': data['email'], 'role': 'admin'}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

# @app.route('/admin/login', methods=['POST'])
# def admin_login():
#     data = request.get_json()
    
#     # Checking the login credentials
#     if data['email'] == 'admin@gmail.com' and data['password'] == 'password':
#         expiration_time = timedelta(hours=1)
#         token = create_access_token(identity='admin', expires_delta=expiration_time)
#         return jsonify({"success": True, "message": "login successful", "token": token, 'user_email': data['email'], 'role': 'admin'}), 200
#     else:
#         return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/register', methods=['POST'])
def register():
    if request.content_type != 'application/json':
        return jsonify({"success": False, "message": "Content-Type must be application/json"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data"}), 400
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    address = data.get('address')
    gender = data.get('gender')
    role = data.get('role')

    if not email or not password or not confirm_password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400

    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match"}), 400

    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"success": False, "message": "Email already registered"}), 400

    # Hash the password
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        address=address,
        gender=gender,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "User registered successfully"}), 201

@app.route('/charities', methods=['GET'])
def view_charities():
        charities = Charity.query.all()
        return jsonify([charity.serialize() for charity in charities])

@app.route('/charities/choose_charity', methods=['POST'])
def choose_charity():
    flash('Charity chosen successfully')
    return redirect(url_for('make_donation'))

# @app.route('/donate', methods=['POST'])
# def make_donation():
#         data = request.json
#         donation = Donation(
#             amount=data.get('amount'),
#             recurring=data.get('recurring', False),
#             is_anonymous=data.get('is_anonymous', False),
#             user_id=current_user.id,
#             charity_id=data.get('charity_id')
#         )
#         db.session.add(donation)
#         db.session.commit()
#         return jsonify({'message': 'Donation successful'})
@app.route('/apply_charity', endpoint='apply_charity_endpoint',methods=['POST'])
def apply_charity():
        data = request.json
        new_charity = Charity(
            name=data.get('name'),
            description=data.get('description'),
            contact_email=data.get('contact_email')
        )
        db.session.add(new_charity)
        db.session.commit()
        return jsonify({'message': 'Charity application submitted successfully'})

@app.route('/non_anonymous_donors', methods=['GET'])
def view_non_anonymous_donors():
        donors = Donation.query.filter_by(is_anonymous=False).all()
        donor_data = [{'donor_name': donor.user.username, 'amount_donated': donor.amount} for donor in donors]
        return jsonify({'non_anonymous_donors': donor_data})

@app.route('/total_donations', methods=['GET'])
def view_total_donations():
        total_donations = sum(donation.amount for donation in Donation.query.all())
        return jsonify({'total_donations': total_donations})

# @app.route('/create_beneficiary_story', endpoint='create_beneficiary_story_endpoint',methods=['POST'])
# def create_beneficiary_story():
#         data = request.json
#         new_story = Beneficiary(
#             name=data.get('name'),
#             content=data.get('content'),
#             charity_id=current_user.id  # Assuming the current user is a Charity
#         )
#         db.session.add(new_story)
#         db.session.commit()
#         return jsonify({'message': 'Beneficiary story posted successfully'})

@app.route('/manage_beneficiaries_inventory', endpoint='manage_beneficiaries_inventory_endpoint', methods=['POST'])
def manage_beneficiaries_inventory():
        data = request.json
        beneficiary = Beneficiary.query.get(data['beneficiary_id'])
        if not beneficiary:
            return jsonify({'message': 'Beneficiary not found'}), 404
        beneficiary.inventory_sent = data['inventory_sent']
        db.session.commit()
        return jsonify({'message': 'Beneficiary inventory updated successfully'})

@app.route('/get_charity_applications', endpoint='get_charity_applications_endpoint',methods=['GET'])
def get_charity_applications():
        charity_applications = Charity.query.filter_by(is_approved=False).all()
        return jsonify({'charity_applications': [charity.serialize() for charity in charity_applications]})

@app.route('/approve_charity/<charity_id>', endpoint='approve_charity_endpoint', methods=['POST'])
def approve_charity(charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return jsonify({'message': 'Charity not found'}), 404
        charity.is_approved = True
        db.session.commit()
        return jsonify({'message': 'Charity application approved successfully'})

@app.route('/reject_charity/<charity_id>', endpoint='reject_charity_endpoint', methods=['POST'])
def reject_charity(charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return jsonify({'message': 'Charity not found'}), 404
        charity.is_approved = False
        db.session.commit()
        return jsonify({'message': 'Charity application rejected successfully'})
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

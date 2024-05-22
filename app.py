from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from datetime import timedelta
from models import db, User
from config import DATABASE_CONFIG  # Import the config
import secrets

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['pw']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['db']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Generate a random secret key
jwt_secret_key = secrets.token_hex(32)  # Generate a 32-byte (256-bit) random key
app.config['JWT_SECRET_KEY'] = jwt_secret_key

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return "This is a basic Flask application"

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    
    # Checking the login credentials
    if data['email'] == 'admin@gmail.com' and data['password'] == 'password':
        expiration_time = timedelta(hours=1)
        token = create_access_token(identity='admin', expires_delta=expiration_time)
        return jsonify({"success": True, "message": "login successful", "token": token, 'user_email': data['email'], 'role': 'admin'}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

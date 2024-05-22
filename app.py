
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from datetime import timedelta
# from models import db, User, Charity, Beneficiary, Transaction, Donor
# from config import DATABASE_CONFIG  # Import the config
import secrets

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['pw']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['db']}"

# Generate a random secret key
jwt_secret_key = secrets.token_hex(32)  # Generate a 32-byte (256-bit) random key

# Set the JWT_SECRET_KEY in your Flask app's configuration
app.config['JWT_SECRET_KEY'] = jwt_secret_key

# Initialize extensions
# db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# URL Routing
@app.route('/')
def index():
    return "This is a basic Flask application"



# Admin LOgin Route with JWT Authentication
@app.route('/adminlogin', methods=['POST'])
def admin_login():
    data = request.get_json()
    
    #checking the login credentials
    if data['email'] == 'admin@gmail.com' and data['password'] == 'password':
       expiration_time =  timedelta(hours=1)
       token = create_access_token(identity='admin', expires_delta=expiration_time)
       
       return jsonify({"success": True, "message": "login successful", "token": token, 'user_email': data['email'], 'role': 'admin'}), 200
   
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    
if __name__ == '__main__':
    app.run(debug=True)

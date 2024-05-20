# from werkzeug.security import check_password_hash, generate_password_hash
# from flask import Flask, request, flash, redirect, url_for, jsonify, g, current_app
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from models import User, Charity, Donation, Beneficiary, Role
# from flask_restful import Api, Resource
# from __init__ import create_app
# from auth import role_required, load_user, init_login_manager

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# from app_routes import *
from app_routes import register_routes
from __init__ import create_app

app = create_app()
register_routes(app)
if __name__ == '__main__':
    app.run(port=5555, debug=True)








# from werkzeug.security import check_password_hash
# from flask import Flask,request,flash,redirect,url_for,jsonify,g, current_app
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from models import User,Charity,Donation,Beneficiary
# from flask_restful import Api,Resource
# from flask_rbac import RBAC

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # rbac = RBAC(app)
# api=Api(app)
# # rbac.set_role_model(Role)
# # rbac.set_user_model(User)
# migrate = Migrate(app, db)
# # ROLE_DONOR='donor'
# # ROLE_ADMINISTRATOR='administrator'
# # ROLE_CHARITY='charity'



# # permissions_donor = [
# #     'view_charities',
# #     'choose_charity',
# #     'make_donation',
# #     'view_beneficiaries',
# #     'donate_via_payment'
# # ]

# # permissions_charity = [
# #     'apply_to_be_charity',
# #     'view_non_anonymous_donors',
# #     'view_anonymous_donors',
# #     'view_total_donations',
# #     'create_beneficiary_stories',
# #     'manage_beneficiaries_inventory'
# # ]
# # permissions_administrator = [
# #     'receive_charity_applications',
# #     'review_charity_applications',
# #     'approve_charity_application',
# #     'reject_charity_application',
# #     'delete_charity'
# # ]

# # roles = {
# #     ROLE_DONOR: Role(ROLE_DONOR, permissions=permissions_donor),
# #     ROLE_CHARITY: Role(ROLE_CHARITY,Permissions=permissions_charity),
# #     ROLE_ADMINISTRATOR: Role(ROLE_ADMINISTRATOR,Permissions=permissions_administrator)
# # }
# # @app.before_first_request
# # def create_tables():
# #     # Create all database tables if they do not exist
# #     db.create_all()


# @app.route('/api/login',methods=['POST'])
# # @rbac.allow(['anonmous'], methods=['POST'])
# def login(email):
#     email = request.json.get('email')
#     password = request.json.get('password')
#     user = User.query.filter_by(email=email).first()
#     if not user or not check_password_hash(user.password, password):
#         return jsonify({'message': 'Invalid email or password'}), 401
#     else:
#         flash('Login successful')
#         return redirect(url_for('home'))
#     g.current_user = user


# @app.route('/api/charities', methods=['GET'])
# # @rbac.allow(['view_charities'])
# def view_charities(name):
#     charities = Charity.query.filter_by(name=name).first()
#     return jsonify(charities.serialize())

# @app.route('/api/charities/choose_charity', methods=['POST'])
# # @rbac.allow(['choose_charity'])
# def choose_charity():

#     flash('Charity chosen successfully')
#     return redirect(url_for('donate'))

# @app.route('/api/donate', methods=['POST'])
# # @rbac.allow(['make_donation'])
# def make_donation():
    
#     return jsonify({'message': 'Donation successful'})
#           # Charity
# @app.route('/api/apply_charity', methods=['POST'])
# # @rbac.allow(['apply_to_be_charity'])
# def apply_charity():
#     # Logic to handle charity application
#     # Example: Save charity details in database
#     data = request.json
#     name=data.get('name')
#     description=data.get('description')
#     contact_email=data.get('contact_email')
#     new_charity=Charity(name=name,description=description,contact_email=contact_email)

#     db.session.add(new_charity)
#     db.session.commit()
#     return jsonify({'message': 'Charity application submitted successfully'})

# @app.route('/api/non_anonymous_donors', methods=['GET'])
# # @rbac.allow(['view_non_anonymous_donors'])
# def view_non_anonymous_donors():
#     # Logic to retrieve and return non-anonymous donors and their donations
#     # Example: Query the database for non-anonymous donors
#     donors = Donation.query.filter_by(is_anonymous=False).all()
#     donor_data = [{'donor_name': donor.donor.name, 'amount_donated': donor.amount} for donor in donors]
#     return jsonify({'non_anonymous_donors': donor_data})

# @app.route('/api/total_donations', methods=['GET'])
# # @rbac.allow(['view_total_donations'])
# def view_total_donations():
#     # Logic to calculate and return the total amount donated to the charity
#     # Example: Query the database to sum up donations
#     total_donations = sum(donation.amount for donation in Donation.query.filter_by(charity_id=Donation.id).all())
#     return jsonify({'total_donations': total_donations})

# @app.route('/api/create_beneficiary_story', methods=['POST'])
# # @rbac.allow(['create_beneficiary_stories'])
# def create_beneficiary_story():
#     # Logic to create and post stories of beneficiaries
#     data = request.json
#     title=data.get('title'),
#     content=data.get('content')
#     new_story=Beneficiary(data=data,title=title,content=content)
#     # Save the beneficiary and story in the database
#     db.session.add(new_story)
#     db.session.commit()
#     return jsonify({'message': 'Beneficiary story posted successfully'})

# @app.route('/api/manage_beneficiaries_inventory', methods=['POST'])
# # @rbac.allow(['manage_beneficiaries_inventory'])
# def manage_beneficiaries_inventory():
#     # Logic to manage beneficiaries and inventory
#     data = request.json
#     beneficiary = Beneficiary.query.get(data['beneficiary_id'])
#     if not beneficiary:
#         return jsonify({'message': 'Beneficiary not found'}), 404
#     beneficiary.inventory_sent = data['inventory_sent']
#     # Update beneficiary inventory in the database
#     db.session.commit()
#     return jsonify({'message': 'Beneficiary inventory updated successfully'})
# #         # ADMINISTRATOR
# @app.route('/api/charity_applications', methods=['GET'])
# # @rbac.allow(['receive_charity_applications'])
# def get_charity_applications():
#     # Logic to retrieve and return list of charity applications
#     charity_applications = Charity.query.filter_by(is_approved=False).all()
#     return jsonify({'charity_applications': [charity.serialize() for charity in charity_applications]})

# @app.route('/api/approve_charity/<int:charity_id>', methods=['POST'])
# # @rbac.allow(['approve_charity_application'])
# def approve_charity(charity_id):
#     # Logic to approve a charity application
#     charity = Charity.query.get(charity_id)
#     if not charity:
#         return jsonify({'message': 'Charity not found'}), 404

#     charity.is_approved = True
#     db.session.commit()
#     return jsonify({'message': 'Charity application approved successfully'})

# @app.route('/api/reject_charity/<int:charity_id>', methods=['POST'])
# # @rbac.allow(['reject_charity_application'])
# def reject_charity(charity_id):
#     try:
#         # Retrieve the charity record from the database
#         charity = Charity.query.get(charity_id)
        
#         # Check if the charity record exists
#         if not charity:
#             return jsonify({'message': 'Charity not found'}), 404

#         # Update the is_approved status to False
#         charity.is_approved = False
#         db.session.commit()

#         return jsonify({'message': 'Charity application rejected successfully'})
#     except Exception as e:
#         # Handle database or other errors
#         db.session.rollback()  # Rollback changes if an error occurs
#         return jsonify({'message': f'Failed to reject charity: {str(e)}'}), 500
# class Register(Resource):
#     def post(self):
#         data = request.json

#         # Retrieve data from JSON payload
#         email = data.get('email')
#         username = data.get('name')
#         password = data.get('password')
#         confirm_password = data.get('confirm_password')  # Correct field name

#         # Basic input validations
#         if not email or len(email) < 4:
#             flash('Email must be valid and greater than 4 characters')
#             return jsonify({"error": "Invalid email"}), 400

#         if not username:
#             flash("Username can't be empty")
#             return jsonify({"error": "Username is required"}), 400

#         if password != confirm_password:
#             flash('Passwords do not match')
#             return jsonify({"error": "Passwords do not match"}), 400

#         # Check if user with the given email already exists
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             return jsonify({"message": "User already exists"}), 409

#         # Create a new user and add to the database
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()

#         # Construct response
#         response_dict = {
#             "id": new_user.id,
#             "username": new_user.username,
#             "email": new_user.email
#         }

#         # Return success response with status code 201
#         return jsonify(response_dict), 201
    
# api.add_resource(Register,'/register')


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)


# def reject_charity(charity_id):
#     # Logic to reject a charity application
#     charity = Charity.query.get(charity_id)
#     if not charity:
#         return jsonify({'message': 'Charity not found'}), 404

#     db.session.delete(charity)
#     db.session.commit()
#     return jsonify({'message': 'Charity application rejected and deleted successfully'})



# from flask import Flask,request,redirect,url_for,jsonify,flash,current_app
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_manager, login_user
# from flask_security import Security, SQLAlchemySessionUserDatastore
# from flask_security import roles_accepted
# from models import User,Role,Charity,Donation,Beneficiary

# app=Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///g4g.sqlite3"
# # needed for session cookies
# app.config['SECRET_KEY'] = 'MY_SECRET'
# # hashes the password and then stores in the database
# app.config['SECURITY_PASSWORD_SALT'] = "MY_SECRET"
# # allows new registrations to application
# app.config['SECURITY_REGISTERABLE'] = True
# # to send automatic registration email to user
# app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
# db = SQLAlchemy()
# db.init_app(app)
# # ctx=current_app._get_current_object()
# @app.before_request
# def before_first_request():
#     db.create_all()

# user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
# security = Security(app, user_datastore)


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     msg=""
#     # if the form is submitted
#     if request.method == 'POST':
#     # check if user already exists
#         user = User.query.filter_by(email=request.form['email']).first()
#         msg=""
#         # if user already exists render the msg
#         if user:
#             return jsonify({"error": "user already exists"})
        
#         # if user doesn't exist
        
#         # store the user to database
#         user = User(email=request.form['email'], active=1, password=request.form['password'])
#         # store the role
#         role = Role.query.filter_by(id=request.form['options']).first()
#         user.roles.append(role)
        
#         # commit the changes to database
#         db.session.add(user)
#         db.session.commit()
        
#         # login the user to the app
#         # this user is current user
#         login_user(user)
#         # redirect to index page
#         return flash('user singed up succesfully')
        
#     # case other than submitting form, like loading the page itself
#     else:
#         return flash('please try to sing up')
    
    


# # signin page
# @app.route('/signin', methods=['GET', 'POST'])
# def signin():

#     if request.method == 'POST':
#         # search user in database
#         user = User.query.filter_by(email=request.form['email']).first()
#         # if exist check password
#         if user:
#             if  user.password == request.form['password']:
#                 # if password matches, login the user
#                 login_user(user)
#                 return redirect(url_for('home'))
#             # if password doesn't match
#             else:
#                 msg="Wrong password"
        
#         # if user does not exist
#         else:
#             flash("User doesn't exist")
#         return redirect(url_for('singup'))
        
#     else:
#         return redirect(url_for('singup'))
        

    
# @app.route('/charity_applications', methods=['GET'])
# @roles_accepted('administrator')
# def get_charity_applications():
#     # Logic to retrieve and return list of charity applications
#     charity_applications = Charity.query.filter_by(is_approved=False).all()
#     return jsonify({'charity_applications': [charity.serialize() for charity in charity_applications]})

# @app.route('/api/approve_charity/<int:charity_id>', methods=['POST'])
# @roles_accepted('administrator')
# def approve_charity(charity_id):
#     # Logic to approve a charity application
#     charity = Charity.query.get(charity_id)
#     if not charity:
#         return jsonify({'message': 'Charity not found'}), 404

#     charity.is_approved = True
#     db.session.commit()
#     return jsonify({'message': 'Charity application approved successfully'})

# @app.route('/reject_charity/<int:charity_id>', methods=['POST'])
# @roles_accepted('administrator')
# def reject_charity(charity_id):
#     try:
#         # Retrieve the charity record from the database
#         charity = Charity.query.get(charity_id)
        
#         # Check if the charity record exists
#         if not charity:
#             return jsonify({'message': 'Charity not found'}), 404

#         # Update the is_approved status to False
#         charity.is_approved = False
#         db.session.commit()

#         return jsonify({'message': 'Charity application rejected successfully'})
#     except Exception as e:
#         # Handle database or other errors
#         db.session.rollback()  # Rollback changes if an error occurs
#         return jsonify({'message': f'Failed to reject charity: {str(e)}'}), 500


# @app.route('/api/apply_charity', methods=['POST'])
# @roles_accepted('charity')
# def apply_charity():
#     # Logic to handle charity application
#     # Example: Save charity details in database
#     data = request.json
#     name=data.get('name')
#     description=data.get('description')
#     contact_email=data.get('contact_email')
#     new_charity=Charity(name=name,description=description,contact_email=contact_email)

#     db.session.add(new_charity)
#     db.session.commit()
#     return jsonify({'message': 'Charity application submitted successfully'})

# @app.route('/api/non_anonymous_donors', methods=['GET'])
# @roles_accepted('charity')
# def view_non_anonymous_donors():
#     # Logic to retrieve and return non-anonymous donors and their donations
#     # Example: Query the database for non-anonymous donors
#     donors = Donation.query.filter_by(is_anonymous=False).all()
#     donor_data = [{'donor_name': donor.donor.name, 'amount_donated': donor.amount} for donor in donors]
#     return jsonify({'non_anonymous_donors': donor_data})

# @app.route('/api/total_donations', methods=['GET'])
# @roles_accepted('charity')
# def view_total_donations():
#     # Logic to calculate and return the total amount donated to the charity
#     # Example: Query the database to sum up donations
#     total_donations = sum(donation.amount for donation in Donation.query.filter_by(charity_id=Donation.id).all())
#     return jsonify({'total_donations': total_donations})

# @app.route('/api/create_beneficiary_story', methods=['POST'])
# @roles_accepted('charity')
# def create_beneficiary_story():
#     # Logic to create and post stories of beneficiaries
#     data = request.json
#     title=data.get('title'),
#     content=data.get('content')
#     new_story=Beneficiary(data=data,title=title,content=content)
#     # Save the beneficiary and story in the database
#     db.session.add(new_story)
#     db.session.commit()
#     return jsonify({'message': 'Beneficiary story posted successfully'})

# @app.route('/api/manage_beneficiaries_inventory', methods=['POST'])
# @roles_accepted('charity')
# def manage_beneficiaries_inventory():
#     # Logic to manage beneficiaries and inventory
#     data = request.json
#     beneficiary = Beneficiary.query.get(data['beneficiary_id'])
#     if not beneficiary:
#         return jsonify({'message': 'Beneficiary not found'}), 404
#     beneficiary.inventory_sent = data['inventory_sent']
#     # Update beneficiary inventory in the database
#     db.session.commit()
#     return jsonify({'message': 'Beneficiary inventory updated successfully'})

# @app.route('/api/charities', methods=['GET'])
# @roles_accepted('donor','administrator')
# def view_charities(name):
#     charities = Charity.query.filter_by(name=name).first()
#     return jsonify(charities.serialize())

# @app.route('/api/charities/choose_charity', methods=['POST'])
# @roles_accepted('donor','administrator')
# def choose_charity():

#     flash('Charity chosen successfully')
#     return redirect(url_for('donate'))

# @app.route('/api/donate', methods=['POST'])
# @roles_accepted('donor','administrator')
# def make_donation():
    
#     return jsonify({'message': 'Donation successful'})



# if __name__ =='__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


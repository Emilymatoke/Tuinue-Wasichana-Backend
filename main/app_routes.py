from flask import flash, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from main.models import db, User, Charity, Donation, Beneficiary
from main.auth import role_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import Api, Resource
from main.roles import Role 

api = Api()

def register_routes(app):
    api.init_app(app)

    @app.route('/login', methods=['POST'])
    def login():
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'message': 'Invalid email or password'}), 401
        login_user(user)
        flash('Login successful')
        return redirect(url_for('home'))

    @app.route('/charities', methods=['GET'])
    @role_required(Role.DONOR)
    def view_charities():
        charities = Charity.query.all()
        return jsonify([charity.serialize() for charity in charities])

    @app.route('/charities/choose_charity', methods=['POST'])
    @login_required
    def choose_charity():
        flash('Charity chosen successfully')
        return redirect(url_for('make_donation'))

    @app.route('/donate', methods=['POST'])
    @login_required
    def make_donation():
        data = request.json
        donation = Donation(
            amount=data.get('amount'),
            recurring=data.get('recurring', False),
            is_anonymous=data.get('is_anonymous', False),
            user_id=current_user.id,
            charity_id=data.get('charity_id')
        )
        db.session.add(donation)
        db.session.commit()
        return jsonify({'message': 'Donation successful'})
    @app.route('/apply_charity', endpoint='apply_charity_endpoint',methods=['POST'])
    @login_required
    @role_required(Role.CHARITY)
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
    @login_required
    def view_non_anonymous_donors():
        donors = Donation.query.filter_by(is_anonymous=False).all()
        donor_data = [{'donor_name': donor.user.username, 'amount_donated': donor.amount} for donor in donors]
        return jsonify({'non_anonymous_donors': donor_data})

    @app.route('/total_donations', methods=['GET'])
    @login_required
    def view_total_donations():
        total_donations = sum(donation.amount for donation in Donation.query.all())
        return jsonify({'total_donations': total_donations})

    @app.route('/create_beneficiary_story', endpoint='create_beneficiary_story_endpoint',methods=['POST'])
    @login_required
    @role_required(Role.CHARITY)
    def create_beneficiary_story():
        data = request.json
        new_story = Beneficiary(
            name=data.get('name'),
            content=data.get('content'),
            charity_id=current_user.id  # Assuming the current user is a Charity
        )
        db.session.add(new_story)
        db.session.commit()
        return jsonify({'message': 'Beneficiary story posted successfully'})

    @app.route('/manage_beneficiaries_inventory', endpoint='manage_beneficiaries_inventory_endpoint', methods=['POST'])
    @login_required
    @role_required(Role.CHARITY)
    def manage_beneficiaries_inventory():
        data = request.json
        beneficiary = Beneficiary.query.get(data['beneficiary_id'])
        if not beneficiary:
            return jsonify({'message': 'Beneficiary not found'}), 404
        beneficiary.inventory_sent = data['inventory_sent']
        db.session.commit()
        return jsonify({'message': 'Beneficiary inventory updated successfully'})

    @app.route('/get_charity_applications', endpoint='get_charity_applications_endpoint',methods=['GET'])
    @login_required
    @role_required(Role.ADMIN)
    def get_charity_applications():
        charity_applications = Charity.query.filter_by(is_approved=False).all()
        return jsonify({'charity_applications': [charity.serialize() for charity in charity_applications]})

    @app.route('/approve_charity/<charity_id>', endpoint='approve_charity_endpoint', methods=['POST'])
    @login_required
    @role_required(Role.ADMIN)
    def approve_charity(charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return jsonify({'message': 'Charity not found'}), 404
        charity.is_approved = True
        db.session.commit()
        return jsonify({'message': 'Charity application approved successfully'})

    @app.route('/reject_charity/<charity_id>', endpoint='reject_charity_endpoint', methods=['POST'])
    @login_required
    @role_required(Role.ADMIN)
    def reject_charity(charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return jsonify({'message': 'Charity not found'}), 404
        charity.is_approved = False
        db.session.commit()
        return jsonify({'message': 'Charity application rejected successfully'})

    class Register(Resource):
        def post(self):
            data = request.json

            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if not email or len(email) < 4:
                flash('Email must be valid and greater than 4 characters')
                return jsonify({"error":
                "Invalid email"}), 400

            if not username:
                flash("Username can't be empty")
                return jsonify({"error": "Username is required"}), 400

            if password != confirm_password:
                flash('Passwords do not match')
                return jsonify({"error": "Passwords do not match"}), 400

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 409

            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            response_dict = {
                "id": new_user.id,  # Corrected attribute name to id
                "username": new_user.username,
                "email": new_user.email
            }

            return jsonify(response_dict), 201

    api.add_resource(Register, '/register')

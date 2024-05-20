from flask import Flask
from models import db
from auth import init_login_manager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    init_login_manager(app)

    with app.app_context():
        db.create_all()

    return app

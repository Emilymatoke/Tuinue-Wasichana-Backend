
from main.app_routes import register_routes
from main import create_app,db

app = create_app()
register_routes(app)
if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(port=5555, debug=True)








# from main.app_routes import register_routes
# from main import create_app,db
from flask import Flask, render_template, request
import stripe  
# import os
from decouple import config

from dotenv import load_dotenv 
# import checkout.html
load_dotenv()


app = Flask(__name__)

stripe_keys = {
        "secret_key": config("STRIPE-SECRETKEY"),
        "publishable_key": config("STRIPE-PUBLISHABLEKEY"),
    }

stripe.api_key = stripe_keys["secret_key"]
print(config("STRIPE-SECRETKEY"))

@app.route('/')
def checkout():
        return render_template('checkout.html',key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
        # Amount in cents
        amount = 2000

        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )

        return render_template('charge.html', amount=amount)


if __name__ == '__main__':
        app.run(debug=True)
        

# app = create_app()
# register_routes(app)
# if __name__ == '__main__':
#     # with app.app_context():
#     #     db.create_all()
#     app.run(port=5555, debug=True)







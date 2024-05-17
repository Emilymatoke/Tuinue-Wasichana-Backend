from flask import Flask, render_template, request
import stripe 
import os
from dotenv import load_dotenv
# import checkout.html
load_dotenv()


app = Flask(__name__)

stripe_keys = {
        "secret_key": os.getenv("STRIPE_SECRET_KEY"),
        "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY"),
    }

stripe.api_key = stripe_keys["secret_key"]

@app.route('/')
def checkout():
        return render_template('checkout.html',key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
        # Amount in cents
        # amount = 1000

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
        app.run()
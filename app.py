import os
import stripe # type: ignore
from flask import Flask, render_template, request

app = Flask(__name__)
stripe_keys = {
        "secret_key": os.environ["sk_test_51PG1q5FormwXQMeHcdCUJ5DDiTBlElrG6Pc1Nr3kI1z6XATepF2eVvXfjQWt4Jea6GvaujpcXNYt7TdfZ4TWyNRj006aEHHgPV"],
        "publishable_key": os.environ["pk_test_51PG1q5FormwXQMeHxbCHD6RehWNOTo1nt2k82ji2F7Cy9aAtS6WmcWTXxedfKFhvFJmBrXxxFqcXdcEJV4kJqhu6004xS7niXh"],
}
stripe.api_key = stripe_keys["secret_key"]

@app.route('/')
def checkout():
        return render_template('checkout.html')

if __name__ == '__main__':
        app.run()
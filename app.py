from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def checkout():
        return render_template('checkout.html')

if __name__ == '__main__':
        app.run()
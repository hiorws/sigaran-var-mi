from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
import sqlite3
from flask import g


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
# sample secret key
app.secret_key = '\x03\x97\xff}\x06\x95\xbc\x1b\x978\xdb\x8b\xfd}\x0e\xeb\x10\xeb\xfe\x172J\x07d'


@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/sigaralar')
def cigarattes():
    cigarette_list = g.db.execute("SELECT * FROM cigarettes").fetchall()
    return render_template('sigaralar.html', cigarettes=cigarette_list)


# homepage
@app.route("/")
def home():
    return render_template('index.html')


def add_cigarette(email, location, amount, price):
    g.db.execute("INSERT INTO cigarettes ('e-mail', 'location', 'amount', 'price') VALUES (?, ?, ?, ?)",
                 [email, location, amount, price])
    g.db.commit()


@app.route("/kayit", methods=["POST"])
def record_cigarette():
    if request.method == "POST":
        location = request.form['location']
        email = request.form['email']
        amount = request.form['dal']
        price_list = request.form.getlist('price')

        price = price_list[0]

        print(location)
        print(email)
        print(amount)
        print(price)
        add_cigarette(email=email, location=location, amount=amount, price=price)
        return render_template('record.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True)

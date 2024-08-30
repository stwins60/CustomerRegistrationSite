from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as mysql
from mysql.connector import Error
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from wtforms import SelectField
import helper
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

alpha_num = "abcdefghijklmnopqrstuvwxyz0123456789"
symbol = "!@#$%^&*()_+"

app.config['SECRET_KEY'] = random.sample(alpha_num+symbol, 16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

error = None
message = None
# host = ""
# password = ""
# username = ""
# Database = ""

db = SQLAlchemy(app)

# try:
#     conn = mysql.connect(host=host, user=username, password=password, database=Database, connect_timeout=6000)
#     cursor = conn.cursor()
#     print("Connected to database")
# except Error as e:
#     error = e

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Customer('{self.name}', '{self.email}', '{self.address}', '{self.country}', '{self.state}', '{self.zip}')"

class RegistrationForm(FlaskForm):
    country = SelectField('Country', choices=helper.get_countries())
    state = SelectField('State', choices=helper.get_states())
    zip = SelectField('Zip Code', choices=helper.get_zip())

@app.route('/')
def index():
    reg_form = RegistrationForm()
    return render_template('index.html', reg_form=reg_form), 200


@app.route('/submit', methods=['POST'])
def submit():
    reg_form = RegistrationForm()
    if request.method == 'POST':
        name = request.form['firstName']
        email = request.form['exampleInputEmail1']
        address = request.form['address']
        country = request.form['country']
        state = request.form['state']
        zip = request.form['zip']

        if country == '' or name == '' or email == '' or address == '' or state == '' or zip == '':
            return render_template('index.html', error='Please enter required fields', reg_form=reg_form)
        else:
            try:
                # cursor.execute("INSERT INTO customers (name, email, address, country, state, zip) VALUES (%s, %s, %s, %s, %s, %s)", (name, email, address, country, state, zip))
                # conn.commit()
                db.session.add(Customers(name=name, email=email, address=address, country=country, state=state, zip=zip))
                db.session.commit()
                print('Data inserted successfully')
                message = "Thank you for your submission. Our team will get back to you soon."
                return render_template('index.html', message=message, reg_form=reg_form), 200
            except Error as e:
                return render_template('index.html', error=e, reg_form=reg_form), 500
            
@app.errorhandler(404)
def page_not_found(e):
    return """
        <html>
            <head>
                <title>Page Not Found</title>
            </head>
            <style>
                body {
                    text-align: center;
                    padding: 150px;
                }
                h1 {
                    font-size: 50px;
                }
                body {
                    font: 20px Helvetica, sans-serif;
                    color: #333;
                }
                article {
                    display: block;
                    text-align: left;
                    width: 650px;
                    margin: 0 auto;
                }
                a {
                    color: #dc8100;
                    text-decoration: none;
                }
                a:hover {
                    color: #333;
                    text-decoration: none;
                }
            </style>
            <body>
                <h1>Page Not Found</h1>
                <p>The page you are looking for does not exist.</p>
                <p><a href="/">Return to the home page</a></p>
            </body>
        </html>
    """, 404
    
@app.errorhandler(500)
def page_not_found(e):
    return """
        <html>
            <head>
                <title>Internal Server Error</title>
            </head>
            <style>
                body {
                    text-align: center;
                    padding: 150px;
                }
                h1 {
                    font-size: 50px;
                }
                body {
                    font: 20px Helvetica, sans-serif;
                    color: #333;
                }
                article {
                    display: block;
                    text-align: left;
                    width: 650px;
                    margin: 0 auto;
                }
                a {
                    color: #dc8100;
                    text-decoration: none;
                }
                a:hover {
                    color: #333;
                    text-decoration: none;
                }
            </style>
            <body>
                <h1>Internal Server Error</h1>
                <p>There was an internal server error. Please try again later.</p>
            </body>
        </html>
    """, 500

@app.errorhandler(405)
def page_not_found(e):
    return """
        <html>
            <head>
                <title>Method Not Allowed</title>
            </head>
            <style>
                body {
                    text-align: center;
                    padding: 150px;
                }
                h1 {
                    font-size: 50px;
                }
                body {
                    font: 20px Helvetica, sans-serif;
                    color: #333;
                }
                article {
                    display: block;
                    text-align: left;
                    width: 650px;
                    margin: 0 auto;
                }
                a {
                    color: #dc8100;
                    text-decoration: none;
                }
                a:hover {
                    color: #333;
                    text-decoration: none;
                }
            </style>
            <body>
                <h1>Method Not Allowed</h1>
                <p>The method you are trying to use is not allowed on this server.</p>
            </body>
        </html>
    """, 405

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

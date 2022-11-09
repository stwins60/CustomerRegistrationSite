from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as mysql
from mysql.connector import Error
from flask_wtf import FlaskForm
from wtforms import SelectField
import AUTH, helper
import random

app = Flask(__name__)
alpha_num = "abcdefghijklmnopqrstuvwxyz0123456789"
symbol = "!@#$%^&*()_+"
app.config['SECRET_KEY'] = random.sample(alpha_num+symbol, 16)
error = None


try:
    conn = mysql.connect(host=AUTH.host, user=AUTH.username, password=AUTH.password, database=AUTH.Database, connect_timeout=6000)
    cursor = conn.cursor()
    print("Connected to database")
except Error as e:
    error = e

class RegistrationForm(FlaskForm):
    country = SelectField('Country', choices=helper.get_countries())
    state = SelectField('State', choices=helper.get_states())
    zip = SelectField('Zip Code', choices=helper.get_zip())

@app.route('/')
def index():
    reg_form = RegistrationForm()
    return render_template('index.html', reg_form=reg_form)


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
                cursor.execute("INSERT INTO customers (name, email, address, country, state, zip) VALUES (%s, %s, %s, %s, %s, %s)", (name, email, address, country, state, zip))
                conn.commit()
                print('Data inserted successfully')
                return redirect(url_for('index'))
            except Error as e:
                return render_template('index.html', error=e, reg_form=reg_form)

if __name__ == '__main__':
    app.run(debug=True)

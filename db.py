import mysql.connector as mysql
import os

DB_USERNAME = os.environ.get('MYSQL_USER')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD')
DB_HOST = os.environ.get('MYSQL_HOST')
DB_DATABASE = os.environ.get('MYSQL_DATABASE')

CONN = mysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, database=DB_DATABASE, connect_timeout=6000)
CURSOR = CONN.cursor()

def create_table():
    try:
        CURSOR.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), address VARCHAR(255), country VARCHAR(255), state VARCHAR(255), zip VARCHAR(255))")
        print("Table created successfully")
    except mysql.Error as e:
        print("Error while creating table: ", e)
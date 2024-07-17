from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os

db_name = os.environ.get('POSTGRES_DB')
user = os.environ.get('POSTGRES_USER')
user_password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')
port = os.environ.get('POSTGRES_PORT')

app = Flask(__name__)

# Setup koneksi ke PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        database = db_name,
        user = user,
        password = user_password,
        host = host,
        port = port
    )
    return conn

# Halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint untuk login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query untuk autentikasi
    cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        flash('Login berhasil', 'success')
        return redirect(url_for('index'))
    else:
        flash('Login gagal, periksa kembali email dan password', 'error')
        return redirect(url_for('index'))

# Endpoint untuk register
@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query untuk insert data user baru
    cursor.execute('INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)',
                   (firstname, lastname, email, password))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Registrasi berhasil, silakan login', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

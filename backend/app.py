from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2

db_name = os.environ.get('POSTGRES_DB')
usr = os.environ.get('POSTGRES_USER')
usr_pwd = os.environ.get('POSTGRES_PASSWORD')
hst = os.environ.get('POSTGRES_HOST')
prt = os.environ.get('POSTGRES_PORT')

app = Flask(__name__)

# Konfigurasi database
db_conn = psycopg2.connect(
    database=db_name,
    user=usr,
    password=usr_pwd,
    host=hst,
    port=prt
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username_or_email = request.form["username_or_email"]
    password = request.form["password"]

    cursor = db_conn.cursor()

    # Cek apakah input mengandung karakter "@"
    if "@" in username_or_email:
        # Jika mengandung "@" maka anggap sebagai email
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", 
                       (username_or_email, password))
    else:
        # Jika tidak mengandung "@" maka anggap sebagai username
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", 
                       (username_or_email, password))

    user = cursor.fetchone()
    cursor.close()

    if user:
        return redirect(url_for("index"))
    else:
        return "Invalid credentials", 401

@app.route("/register", methods=["POST"])
def register():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    password = request.form["password"]

    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)", 
                   (firstname, lastname, email, password))
    db_conn.commit()
    cursor.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

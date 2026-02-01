from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "securekey123"
bcrypt = Bcrypt(app)


def get_db():
    return sqlite3.connect("database.db")

def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT)""")
    db.commit()
    db.close()

@app.route("/", methods=["GET", "POST"])
def login():
    user = None   # ✅ FIX

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT password FROM users WHERE email=?",
            (email,)
        )
        user = cur.fetchone()
        db.close()

        if user and bcrypt.check_password_hash(user[0], password):
            session["user"] = email
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )
        db.commit()
        db.close()

        return redirect("/")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
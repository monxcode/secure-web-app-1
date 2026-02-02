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

    # Create users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    #  Create default admin (one-time)
    cur.execute("SELECT * FROM users WHERE role='admin'")
    admin = cur.fetchone()

    if not admin:
        hashed = bcrypt.generate_password_hash("admin123").decode("utf-8")
        cur.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            ("admin@secureapp.com", hashed, "admin")
        )

    db.commit()
    db.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT password, role FROM users WHERE email=?",
            (email,)
        )
        user = cur.fetchone()
        db.close()

        if user and bcrypt.check_password_hash(user[0], password):
            session["email"] = email
            session["role"] = user[1]

            if user[1] == "admin":
                return redirect("/admin")
            else:
                return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    # GET request (page load)
    return render_template("login.html")

    # GET request (page load)
    return render_template("login.html")

@app.route("/admin")
def admin():
    if "email" not in session or session.get("role") != "admin":
        return redirect("/")
    return render_template("admin.html")

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
    if "email" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
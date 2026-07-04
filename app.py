from flask import Flask, render_template, request, redirect, session
import pymysql
from config import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "cloudlms_secret_key"


@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Student Registration
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Hash the password
        hashed_password = generate_password_hash(password)

        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        sql = """
        INSERT INTO students(name, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (name, email, hashed_password))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/")

    return render_template("register.html")


# -----------------------------
# Student Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        sql = "SELECT * FROM students WHERE email=%s"
        cursor.execute(sql, (email,))

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        if student:

            stored_password = student[3]

            if check_password_hash(stored_password, password):

                session["student"] = student[1]

                return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "student" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        student=session["student"]
    )


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.pop("student", None)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

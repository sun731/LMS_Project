from flask import Blueprint, render_template, request, redirect, session
import pymysql

from config import *
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/")
def home():
    return render_template("index.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

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


@auth.route("/login", methods=["GET", "POST"])
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

        cursor.execute(
            "SELECT * FROM students WHERE email=%s",
            (email,)
        )

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        if student:

            if check_password_hash(student[3], password):

                session["student"] = student[1]

                return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


@auth.route("/dashboard")
def dashboard():

    if "student" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        student=session["student"]
    )


@auth.route("/logout")
def logout():

    session.pop("student", None)

    return redirect("/")

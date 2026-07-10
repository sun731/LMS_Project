from flask import Blueprint, render_template, request, redirect, session, flash, abort
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

        cursor.execute(
            """
            INSERT INTO students(name, email, password)
            VALUES(%s, %s, %s)
            """,
            (name, email, hashed_password)
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Registration successful! Please login.", "success")

        return redirect("/login")

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
                session["student_id"] = student[0]
                session["role"] = student[4]

                flash(f"Welcome, {student[1]}!", "success")

                return redirect("/dashboard")

        flash("Invalid Email or Password.", "danger")

        return redirect("/login")

    return render_template("login.html")


@auth.route("/dashboard")
def dashboard():

    if "student" not in session:
        return redirect("/login")

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM enrollments")
    total_enrollments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM materials")
    total_materials = cursor.fetchone()[0]

    cursor.execute("""
        SELECT course_name, instructor
        FROM courses
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        student=session["student"],
        total_students=total_students,
        total_courses=total_courses,
        total_enrollments=total_enrollments,
        total_materials=total_materials,
        recent_courses=recent_courses
    )

@auth.route("/admin")
def admin():

    if "student" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        abort(403)

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, password, role
        FROM students
        ORDER BY id
    """)

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin.html",
        users=users
    )

@auth.route("/profile")
def profile():

    if "student" not in session:
        return redirect("/login")

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (session["student_id"],)
    )

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "profile.html",
        student=student
    )

@auth.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out successfully.", "info")

    return redirect("/login")

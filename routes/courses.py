from flask import Blueprint, render_template, request, redirect, session, flash, abort
import pymysql
from config import *

courses = Blueprint("courses", __name__)


@courses.route("/courses")
def view_courses():

    if "student" not in session:
        return redirect("/login")

    search = request.args.get("search", "").strip()

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    if search:

        cursor.execute(
            """
            SELECT * FROM courses
            WHERE course_name LIKE %s
            """,
            ("%" + search + "%",)
        )

    else:

        cursor.execute("SELECT * FROM courses")

    course_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "courses.html",
        courses=course_list,
        search=search
    )

@courses.route("/courses/add", methods=["GET", "POST"])
def add_course():

    if "student" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        abort(403)

    if request.method == "POST":

        course_name = request.form["course_name"]
        instructor = request.form["instructor"]
        description = request.form["description"]

        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        # Check for duplicate course
        cursor.execute(
            "SELECT * FROM courses WHERE course_name=%s",
            (course_name,)
        )

        existing = cursor.fetchone()

        if existing:

            cursor.close()
            connection.close()

            flash("Course already exists.", "warning")

            return redirect("/courses/add")

        cursor.execute(
            """
            INSERT INTO courses(course_name, instructor, description)
            VALUES(%s, %s, %s)
            """,
            (course_name, instructor, description)
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Course added successfully!", "success")

        return redirect("/courses")

    return render_template("add_course.html")


@courses.route("/courses/edit/<int:id>", methods=["GET", "POST"])
def edit_course(id):

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

    if request.method == "POST":

        course_name = request.form["course_name"]
        instructor = request.form["instructor"]
        description = request.form["description"]

        cursor.execute(
            """
            UPDATE courses
            SET course_name=%s,
                instructor=%s,
                description=%s
            WHERE id=%s
            """,
            (course_name, instructor, description, id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Course updated successfully!", "success")

        return redirect("/courses")

    cursor.execute(
        "SELECT * FROM courses WHERE id=%s",
        (id,)
    )

    course = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_course.html",
        course=course
    )


@courses.route("/courses/delete/<int:id>")
def delete_course(id):

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

    cursor.execute(
        "DELETE FROM courses WHERE id=%s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    flash("Course deleted successfully!", "warning")

    return redirect("/courses")

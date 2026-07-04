from flask import Blueprint, render_template, request, redirect
import pymysql
from config import *

courses = Blueprint("courses", __name__)


@courses.route("/courses")
def view_courses():

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM courses")

    course_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "courses.html",
        courses=course_list
    )


@courses.route("/courses/add", methods=["GET", "POST"])
def add_course():

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

        sql = """
        INSERT INTO courses(course_name, instructor, description)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            sql,
            (course_name, instructor, description)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/courses")

    return render_template("add_course.html")
@courses.route("/courses/edit/<int:id>", methods=["GET", "POST"])
def edit_course(id):

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

        sql = """
        UPDATE courses
        SET course_name=%s,
            instructor=%s,
            description=%s
        WHERE id=%s
        """

        cursor.execute(
            sql,
            (course_name, instructor, description, id)
        )

        connection.commit()

        cursor.close()
        connection.close()

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

    return redirect("/courses")

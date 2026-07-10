from flask import Blueprint, render_template, session, redirect, flash
import pymysql
from config import *

enrollments = Blueprint("enrollments", __name__)


@enrollments.route("/mycourses")
def my_courses():

    if "student" not in session:
        return redirect("/login")

    student_id = session["student_id"]

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT courses.course_name,
               courses.instructor,
               courses.description
        FROM courses
        INNER JOIN enrollments
            ON courses.id = enrollments.course_id
        WHERE enrollments.student_id = %s
    """, (student_id,))

    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "my_courses.html",
        courses=courses
    )


@enrollments.route("/enroll/<int:course_id>")
def enroll(course_id):

    if "student" not in session:
        return redirect("/login")

    student_id = session["student_id"]

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM enrollments
        WHERE student_id=%s AND course_id=%s
        """,
        (student_id, course_id)
    )

    existing = cursor.fetchone()

    if existing:

        flash("You are already enrolled in this course.", "warning")

    else:

        cursor.execute(
            """
            INSERT INTO enrollments(student_id, course_id)
            VALUES(%s, %s)
            """,
            (student_id, course_id)
        )

        connection.commit()

        flash("Enrollment successful!", "success")

    cursor.close()
    connection.close()

    return redirect("/mycourses")


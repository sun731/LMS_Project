from flask import Blueprint, render_template, request, redirect, session, flash
import pymysql
import boto3
from botocore.client import Config
from config import *

assignments = Blueprint("assignments", __name__)

# S3 Client
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    config=Config(signature_version="s3v4")
)


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@assignments.route("/assignments")
def my_assignments():

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
        SELECT assignments.title,
               courses.course_name,
               assignments.filename,
               assignments.submitted_at
        FROM assignments
        INNER JOIN courses
            ON assignments.course_id = courses.id
        WHERE assignments.student_id=%s
        ORDER BY assignments.submitted_at DESC
    """, (student_id,))

    assignment_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "my_assignments.html",
        assignments=assignment_list
    )


@assignments.route("/assignments/upload", methods=["GET", "POST"])
def upload_assignment():

    if "student" not in session:
        return redirect("/login")

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        course_id = request.form["course_id"]

        file = request.files["file"]
        filename = file.filename

        if not allowed_file(filename):

            flash(
                "Only PDF, DOC, DOCX, PPT, PPTX and TXT files are allowed.",
                "danger"
            )

            cursor.close()
            connection.close()

            return redirect("/assignments/upload")

        # Upload to S3
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            filename
        )

        cursor.execute("""
            INSERT INTO assignments
            (student_id, course_id, title, filename)
            VALUES(%s,%s,%s,%s)
        """,
        (
            session["student_id"],
            course_id,
            title,
            filename
        ))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Assignment submitted successfully!", "success")

        return redirect("/assignments")

    cursor.execute("SELECT id, course_name FROM courses")

    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "upload_assignment.html",
        courses=courses
    )

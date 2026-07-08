from flask import Blueprint, render_template, session, redirect, request
import pymysql
import boto3
from botocore.client import Config
from config import *

materials = Blueprint("materials", __name__)

# Create S3 client
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    config=Config(signature_version="s3v4")
)


@materials.route("/materials")
def view_materials():

    if "student" not in session:
        return redirect("/login")

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT materials.id,
               materials.title,
               materials.filename,
               courses.course_name
        FROM materials
        INNER JOIN courses
        ON materials.course_id = courses.id
    """)

    materials_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "materials.html",
        materials=materials_list
    )


@materials.route("/materials/upload", methods=["GET", "POST"])
def upload_material():

    if "student" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access Denied", 403

    if request.method == "POST":

        title = request.form["title"]
        course_id = request.form["course_id"]

        file = request.files["file"]
        filename = file.filename

        # Upload file to Amazon S3
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            filename
        )

        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO materials(course_id, title, filename)
            VALUES(%s, %s, %s)
            """,
            (course_id, title, filename)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/materials")

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM courses")

    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "upload_material.html",
        courses=courses
    )


@materials.route("/materials/download/<filename>")
def download_material(filename):

    if "student" not in session:
        return redirect("/login")

    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": filename
        },
        ExpiresIn=300
    )

    return redirect(url)

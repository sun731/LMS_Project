from flask import Blueprint, render_template, session, redirect, request, send_from_directory
import pymysql
import os
from config import *

materials = Blueprint("materials", __name__)


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

    if request.method == "POST":

        title = request.form["title"]
        course_id = request.form["course_id"]

        file = request.files["file"]

        filename = file.filename

        file.save(os.path.join("uploads", filename))

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

    return send_from_directory(
        "uploads",
        filename,
        as_attachment=True
    )

from flask import Blueprint, render_template, request, redirect, session, flash, abort
import pymysql
from config import *

announcements = Blueprint("announcements", __name__)


@announcements.route("/announcements")
def view_announcements():

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
        SELECT *
        FROM announcements
        ORDER BY created_at DESC
    """)

    announcement_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "announcements.html",
        announcements=announcement_list
    )


@announcements.route("/announcements/add", methods=["GET", "POST"])
def add_announcement():

    if "student" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        abort(403)

    if request.method == "POST":

        title = request.form["title"]
        message = request.form["message"]

        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO announcements(title, message)
            VALUES(%s,%s)
        """, (title, message))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Announcement posted successfully!", "success")

        return redirect("/announcements")

    return render_template("add_announcement.html")

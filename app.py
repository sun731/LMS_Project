from flask import Flask, render_template
from routes.auth import auth
from routes.courses import courses
from routes.enrollments import enrollments
from routes.materials import materials
from routes.assignments import assignments
from routes.announcements import announcements

app = Flask(__name__)
app.secret_key = "cloudlms_secret_key"

app.register_blueprint(auth)
app.register_blueprint(courses)
app.register_blueprint(enrollments)
app.register_blueprint(materials)
app.register_blueprint(assignments)
app.register_blueprint(announcements)
@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

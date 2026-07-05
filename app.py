from flask import Flask
from routes.auth import auth
from routes.courses import courses
from routes.enrollments import enrollments
from routes.materials import materials

app = Flask(__name__)
app.secret_key = "cloudlms_secret_key"

app.register_blueprint(auth)
app.register_blueprint(courses)
app.register_blueprint(enrollments)
app.register_blueprint(materials)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask
from routes.auth import auth
from routes.courses import courses
from routes.enrollments import enrollments

app = Flask(__name__)
app.secret_key = "cloudlms_secret_key"

app.register_blueprint(auth)
app.register_blueprint(courses)
app.register_blueprint(enrollments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

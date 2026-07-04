from flask import Flask
from routes.auth import auth

app = Flask(__name__)
app.secret_key = "cloudlms_secret_key"

app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

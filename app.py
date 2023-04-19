import os
import secrets

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "images")


@app.route("/")
def index():
    return "Hello,Flaskbook!"


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(filename)
    new_filename = random_hex + ext
    print(app.config["UPLOAD_FOLDER"])
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], new_filename))
    return jsonify({"message": "File uploaded successfully."}), 200

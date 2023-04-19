import os
import secrets

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "images")
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

ALLOWED_EXTENSIONS = {"jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return "Hello,Flaskbook!"


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        random_hex = secrets.token_hex(8)
        _, ext = os.path.splitext(filename)
        new_filename = random_hex + ext
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], new_filename))
        return jsonify({"message": "File uploaded successfully."}), 200
    else:
        return jsonify({"message": "invalid file."}), 200

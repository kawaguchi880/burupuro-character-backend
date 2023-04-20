import os
import secrets

from azure.storage.blob import BlobClient, BlobServiceClient
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "images")
connection_string = os.environ["CONNECTION_STRING"]
container_name = os.environ["CONTAINER_NAME"]


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
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
    file.save(file_path)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    with open(file_path, "rb") as data:
        blob_client = container_client.upload_blob(name=new_filename, data=data)
    os.remove(file_path)
    blob_url = blob_client .url
    print(blob_url)
    return jsonify({"message": "File uploaded successfully."}), 200

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello,Flaskbook!"


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/hello")
def tekitou():
    return "こんにちは！川口遥生さん！！"

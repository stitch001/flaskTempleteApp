
from flask import Flask, render_template
from flask import jsonify, request

from loguru import logger

from flask_sqlalchemy import SQLAlchemy

from api.user_api import get_user_api
from api.todoitem_api import get_todoitem_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mysql@127.0.0.1:3306/todolist?charset=utf8"
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

user_api = get_user_api(app, db)
todoitem_api = get_todoitem_api(app, db)
app.register_blueprint(user_api)
app.register_blueprint(todoitem_api)


@app.route('/')
def hello_world():
    logger.info(request.headers["Head1"])
    return render_template('hello.html')


@app.route('/hello')
def hello():
    return "<h1>hello flask</h1>"


@app.route('/post', methods=["POST"])
def get_post():
    name = request.values.get("name")
    logger.info(name)
    return "hello" + name


@app.route("/postjson", methods=["POST"])
def get_json():
    data = request.get_json()
    data["age"] = int(data["age"]) + 1
    return jsonify(data)


if __name__ == '__main__':
    app.run()

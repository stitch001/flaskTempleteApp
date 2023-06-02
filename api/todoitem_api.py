from loguru import logger
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify,request
from flask import Blueprint
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
todoitem_api = Blueprint("todoitem_api", __name__, url_prefix="/api/todoitem")

db_session = None
Base = declarative_base()


class Todoitem(Base):
    __tablename__ = "todoitem"
    id = Column(Integer, primary_key=True,
                autoincrement=True, comment="自增主键")
    title = Column(String(
        100), nullable=False, comment="标题")
    content = Column(
        String(100), nullable=False, comment="内容")
    duedate = Column(
        Date(), nullable=False, comment="内容")
    user_id = Column(Integer, autoincrement=True, comment="自增主键")

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "duedate": self.duedate,
            "user_id": self.user_id
        }


@todoitem_api.route('/id/<todoitemid>', methods=['GET'])
def get_item_by_id(todoitemid: int):
    item = db_session.query(Todoitem).filter_by(id=todoitemid).first()
    logger.info(f"access /user/{todoitemid}")
    if item:
        return jsonify(item.to_json())
    else:
        return jsonify({})

@todoitem_api.route('/list', methods=['GET'])
def get_items():
    userid = request.args.get("user")
    if not userid:
        return jsonify({})
    item_list = db_session.query(Todoitem).filter_by(user_id=userid)
    item_out = [item.to_json() for item in item_list]
    logger.info(f"query item by userid {userid}")
    return jsonify(item_out)


@todoitem_api.route('/all', methods=['GET'])
def get_item_all():
    items = db_session.query(Todoitem).all()
    items_out = [item.to_json() for item in items]
    if items:
        return jsonify(items_out)
    else:
        return jsonify({})


def get_todoitem_api(app, db):
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        global db_session
        db_session = Session()
    return todoitem_api

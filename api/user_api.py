from loguru import logger
from sqlalchemy.orm import sessionmaker
from flask import jsonify, request
from flask import Blueprint
from sqlalchemy import Column, Integer, String,Date
from sqlalchemy.orm import declarative_base

user_api = Blueprint("api", __name__, url_prefix="/api/user")

db_session = None


Base = declarative_base()

class Sys_user(Base):
    __tablename__ = "sys_user"
    id = Column(Integer, primary_key=True,
                autoincrement=True, comment="自增主键")
    username = Column(String(
        100), nullable=False, comment="用户名")
    password = Column(
        String(100), nullable=False, comment="密码")
    email = Column(String(
        100), nullable=False, comment="电子邮箱", unique=True)
    
    def to_json(self):
        return {
            "id":self.id,
            "username":self.username,
            "password":self.password,
            "email":self.email
        }

@user_api.route('/id/<userid>', methods=['GET'])
def get_user(userid: int):
    user1 = db_session.query(Sys_user).filter_by(id=userid).first()
    logger.debug(f"access /user/{userid}")
    if user1:
        return jsonify(user1.to_json())
    else:
        return jsonify({})


def get_user_api(app, db):
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        global db_session
        db_session = Session()
    return user_api

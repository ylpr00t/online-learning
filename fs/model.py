from fs.init_db import db
import datetime
from werkzeug.security import  generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'ak_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=False, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(64), nullable=False, default='normal')# normal, delete

    # 将get和set方法变成属性,这里的password不直接对外暴露,只能通过setter将pshash存入数据库
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserInfo(db.Model):
    __tablename__ = 'ak_userinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('ak_user.id'), nullable=False)
    real_name = db.Column(db.String(128), nullable=False)
    user_email = db.Column(db.String(128), nullable=False)
    user_address = db.Column(db.String(128), nullable=False)


class Classes(db.Model):
    __tablename__ = 'ak_classes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("ak_user.id"), nullable=False)
    rand_num = db.Column(db.String(6), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    explain = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='normal')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())


class Resources(db.Model):
    __tablename__ = 'ak_resources'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classes_id = db.Column(db.Integer, db.ForeignKey("ak_classes.id"), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(128), nullable=False) # 资料描述
    category = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(1024), nullable=False)
    e_coin = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(10), nullable=False, default='normal')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())


class Study(db.Model):
    __tablename__ = 'ak_study'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("ak_user.id"), nullable=False)
    classes_id = db.Column(db.Integer, db.ForeignKey("ak_classes.id"), nullable=False)
    e_coin = db.Column(db.Integer, nullable=False, default=0)
    explain = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='normal')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())


class StudyTrace(db.Model):
    __tablename__ = 'ak_study_trace'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    study_id = db.Column(db.Integer, db.ForeignKey("ak_study.id"), nullable=False)
    study_ecoin = db.Column(db.Integer, nullable=False)
    study_info = db.Column(db.String(1024), nullable=False, default='empty')
    status = db.Column(db.String(10), nullable=False, default='normal')
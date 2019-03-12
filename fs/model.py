from fs.init_db import db
from werkzeug.security import  generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'ak_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=True)
    status = db.Column(db.String(64), nullable=False, default='normal')# normal, delete

    #将get和set方法变成属性,这里的password不直接对外暴露,只能通过setter将pshash存入数据库
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
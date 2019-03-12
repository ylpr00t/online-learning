from flask_script import Manager, Server
from fs.init_app import app
from fs.init_jwt import jwt
from fs.init_db import db
from fs.api import api


# 挂上app
db.init_app(app)
jwt.init_app(app)
api.bind_app(app)

# 以下是启动参数
manager = Manager(app)


@manager.command
def create_tables():
    """建表"""
    # 不导入无法创建表,奇怪
    from fs import model
    db.create_all()


@manager.command
def drop_tables():
    """删除表"""
    # 不导入无法删除表,奇怪
    from fs import model
    db.drop_all()


manager.add_command('runserver', Server(port=8080, host='127.0.0.1'))


if __name__ == '__main__':
    manager.run()
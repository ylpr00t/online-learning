import flask_restful as restful
from sqlalchemy import func
from flask_jwt import current_identity, jwt_required
from fs.utils import format_response
from fs.init_db import db
from fs import model


class ApiMyInfo(restful.Resource):
    @jwt_required()
    def post(self):
        assert current_identity is not None
        user_id = int(current_identity)
        userinfo = db.session.query(model.User) \
                .outerjoin(model.UserInfo, model.User.id == model.UserInfo.user_id) \
                .filter(model.User.id == user_id) \
                .with_entities(model.User.username,
                               model.UserInfo.real_name,
                               model.UserInfo.user_email,
                               model.UserInfo.user_address).first()

        format_userinfo = {}
        format_userinfo['username'] = userinfo[0] if userinfo[0] else 'undefined'
        format_userinfo['realname'] = userinfo[1] if userinfo[1] else 'undefined'
        format_userinfo['useremail'] = userinfo[2] if userinfo[2] else 'undefined'
        format_userinfo['useraddress'] = userinfo[3] if userinfo[3] else 'undefined'
        format_userinfo['classes_num'] = 10
        format_userinfo['category'] = ['数学', '计算机', '金融']
        return format_response(0, 'success', {'myinfo': format_userinfo})
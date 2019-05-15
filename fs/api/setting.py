import flask_restful as restful
from flask_restful import reqparse
from flask_jwt import current_identity, jwt_required
from fs.utils import format_response
from fs.init_db import db
from fs import model


class ApiSetting(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('realname', type=str, location='json', required=True)
        self.reqparser.add_argument('useremail', type=str, location='json', required=True)
        self.reqparser.add_argument('useraddress', type=str, location='json', required=True)

    @jwt_required()
    def post(self):
        assert current_identity is not None

        args = self.reqparser.parse_args()
        user_id = int(current_identity)

        real_name = args.get('realname', None)
        user_email = args.get('useremail', None)
        user_address = args.get('useraddress', None)

        if real_name == '' or user_email == '' or user_address == '':
            return format_response(-400, '请检查参数')

        u = model.UserInfo()
        u.user_id = user_id
        u.real_name = real_name
        u.user_email = user_email
        u.user_address = user_address
        db.session.add(u)
        db.session.commit()
        return format_response(0, 'success')

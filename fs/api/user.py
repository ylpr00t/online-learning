import flask_restful as restful
from flask_restful import reqparse
from flask_jwt import current_identity, jwt_required
from flask import jsonify
from fs.utils import format_response
from fs.init_jwt import jwt
from fs.init_db import db
from fs import model


class ApiRegister(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('username', type=str, location='json', required=True)
        self.reqparser.add_argument('password', type=str, location='json', required=True)

    def post(self):
        args = self.reqparser.parse_args()
        #验证用户名和密码格式
        '''
        verify username and password
        user:15591470327
        pass:1
        '''
        u = model.User()
        u.username = args.get('username', 'noname')
        u.password = args.get('password', 'nopass')
        u.status = 'normal'
        db.session.add(u)
        db.session.commit()
        return jsonify(format_response(0, 'success'))


class ApiLogin(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('username', type=str, location='json', required=True)
        self.reqparser.add_argument('password', type=str, location='json', required=True)

    def post(self):
        args = self.reqparser.parse_args()
        #jwt.authentication_callback返回值必须具有id属性
        identity = jwt.authentication_callback(args['username'], args['password'])
        if not identity or len(args['password']) > 16:
            return format_response(-400, 'bad password')
        access_token = jwt.jwt_encode_callback(identity)
        return format_response(0, 'success', {
            'access_token':str(access_token, 'utf-8'),
        })


class ApiUserList(restful.Resource):
    @jwt_required()
    def post(selfs):
        assert current_identity is not None
        user_id = int(current_identity)
        return format_response(0, 'success', user_id)
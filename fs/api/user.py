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
        # jwt.authentication_callback返回值必须具有id属性
        identity = jwt.authentication_callback(args['username'], args['password'])
        if not identity or len(args['password']) > 16:
            return format_response(-400, 'bad password')
        access_token = jwt.jwt_encode_callback(identity)
        if args['username'] == 'admin':
            return format_response(0, 'success', {
                'super_token': str(access_token, 'utf-8'),
                'administrator': True,
            })
        else:
            return format_response(0, 'success', {
                'access_token':str(access_token, 'utf-8'),
                'administrator': False,
            })


# 管理员权限
class ApiUserList(restful.Resource):
    @jwt_required()
    def post(self):
        assert current_identity is not None
        user_id = int(current_identity)
        admin_user = model.User.query.filter_by(id=user_id).first()
        if admin_user is not None:
            if admin_user.is_admin != 1:
                return format_response(-400, 'wraning', '权限不足')

        users = model.User.query.filter_by(status='normal').all()
        format_users = []
        for user in users:
            if user.is_admin == 1:
                continue
            item_dict = {}
            item_dict['value'] = user.username
            item_dict['label'] = user.username
            format_users.append(item_dict)
        return format_response(0, 'success', {'users': format_users})


class ApiIsAdmin(restful.Resource):


    @jwt_required()
    def post(self):
        assert current_identity is not None
        user_id = int(current_identity)
        user = model.User.query.filter_by(id=user_id).first()
        if user is None:
            return format_response(-400, '没有此用户', '没有此用户')
        if user.is_admin == 1:
            return format_response(0, 'success', {
                'is_amdin': True
            })
        else:
            return format_response(0, 'success', {
                'is_admin': False
            })


class ApiSuperSwitch(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('username', type=str, location='json', required=True)

    @jwt_required()
    def post(self):
        assert current_identity is not None
        user_id = int(current_identity)
        args = self.reqparser.parse_args()
        user = model.User.query.filter_by(id=user_id).first()
        if user is None:
            return format_response(-400, '用户ID无效', '用户ID无效')
        if user.is_admin != 1:
            return format_response(-400, '用户权限不足', '用户权限不足')

        # password
        identifity = jwt.authentication_callback(args['username'], 'g1HL641qJ8zqGpWUdeR3JPriZYenGHrGOUtbzkdwHZ7OdaEBRLE1JMpPnJ2eVxcjx3svuJE2QV3lPoknjU1ZbdAaXykDVel8EmBihYj95tIfbseeT673AS9A2KrYDCl8aJHJ5JyAtQCZDRIJcEh9Yj7ufEtGcXO0lPd3JLNwayg3QioWyNHb2l1GXXCyktBI7HTeQD')
        if not identifity:
            return format_response(-400, '无该用户', '无该用户')
        access_token = jwt.jwt_encode_callback(identifity)
        return format_response(0, 'success', {
            'access_token': str(access_token, 'utf-8'),
        })
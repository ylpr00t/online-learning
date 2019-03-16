import flask_restful as restful
from flask_jwt import current_identity, jwt_required
from flask_restful import reqparse
from fs.utils import format_response


class Index(restful.Resource):
    def get(self):
        return 'welcome to ylp restful'


class ApiIsLogin(restful.Resource):
    @jwt_required()
    def post(self):
        assert current_identity is not None
        return format_response(0, 'success', str(int(current_identity)))
import flask_restful as restful
from flask_restful import reqparse
from flask_jwt import current_identity, jwt_required
from fs.utils import format_response
from fs.init_db import db
from fs import model
from fs import config
import random
import datetime


class ApiAddClasses(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('name', type=str, location='json', required=True)
        self.reqparser.add_argument('category', type=int, location='json', required=True)
        self.reqparser.add_argument('explain', type=str, location='json', required=True)

    @jwt_required()
    def post(self):
        assert current_identity is not None

        args = self.reqparser.parse_args()
        user_id = int(current_identity)
        rand_num = ''
        for i in range(6):
            rand_num += str(random.randint(0, 9))
        name = args.get('name', None)
        category = args.get('category', None)
        explain = args.get('explain', None)
        create_time = datetime.datetime.now()

        if name == '' or category == '' or explain == '' or category not in config.CLASSES_CATEGORY:
            return format_response(-400, '请检查参数')

        c = model.Classes()
        c.user_id = user_id
        c.rand_num = rand_num
        c.name = name
        c.category = category
        c.explain = explain
        c.create_time = create_time
        db.session.add(c)
        db.session.commit()
        return format_response(0, 'success')

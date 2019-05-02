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


class ApiMyClass(restful.Resource):
    @jwt_required()
    def post(self):
        assert current_identity is not None
        user_id = int(current_identity)
        classes = db.session.query(model.Classes) \
                .filter(model.Classes.user_id == user_id) \
                .filter(model.Classes.status == 'normal') \
                .all()
        format_classes = []
        for item in classes:
            item_dict = {}
            item_dict['id'] = item.id
            item_dict['name'] = item.name
            item_dict['rand_num'] = item.rand_num
            item_dict['create_date'] = item.create_time.strftime("%Y-%m-%d %H:%M:%S")
            format_classes.append(item_dict)
        return format_response(0, 'success', {'myclasses': format_classes})


class ApiAddResource(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('classes_id', type=int, location='json', required=True)
        self.reqparser.add_argument('name', type=str, location='json', required=True)
        self.reqparser.add_argument('category', type=int, location='json', required=True)
        self.reqparser.add_argument('desc', type=str, location='json', required=True)
        self.reqparser.add_argument('content', type=str, location='json', required=True)
    @jwt_required()
    def post(self):
        assert current_identity is not None
        args = self.reqparser.parse_args()
        user_id = int(current_identity)
        classes_id = args.get('classes_id', -1)
        classes = db.session.query(model.Classes) \
                .filter(model.Classes.user_id == user_id) \
                .filter(model.Classes.id == classes_id) \
                .filter(model.Classes.status == 'normal') \
                .first()
        if classes is None:
            return format_response(-400, '此用户没有该课程')

        name = args.get('name', '')
        category = args.get('category', -1)
        desc = args.get('desc', '')
        content = args.get('content', '')
        if name == '' or desc == '' or content == '' or category not in config.RESOURCE_CATEGORY:
            return format_response(-400, '请检查提交的参数')

        r = model.Resources()
        r.classes_id = classes_id
        r.name = name
        r.category = category
        r.desc = desc
        r.content = content
        r.create_time = datetime.datetime.now()
        db.session.add(r)
        db.session.commit()
        return format_response(0, 'success')


class ApiMyResources(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('classes_id', type=int, location='json', required=True)
    @jwt_required()
    def post(self):
        assert current_identity is not None
        args = self.reqparser.parse_args()
        user_id = int(current_identity)
        classes_id = args.get('classes_id', -1)
        classes = db.session.query(model.Classes) \
                .filter(model.Classes.user_id == user_id) \
                .filter(model.Classes.id == classes_id) \
                .filter(model.Classes.status == 'normal') \
                .first()
        if classes is None:
            return format_response(-400, '此用户没有该课程')

        resources = db.session.query(model.Resources) \
                .filter(model.Resources.classes_id == classes_id) \
                .filter(model.Resources.status == 'normal') \
                .all()

        format_resources = []
        for r in resources:
            r_item = {}
            r_item['id'] = r.id
            r_item['name'] = r.name
            r_item['category'] = r.category
            r_item['desc'] = r.desc
            r_item['content'] = r.content
            r_item['create_time'] = r.create_time.strftime("%Y-%m-%d %H:%M:%S")
            format_resources.append(r_item)
        return format_response(0, 'success', {'myresources': format_resources})

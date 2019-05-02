import flask_restful as restful
from flask_restful import reqparse
from flask_jwt import current_identity, jwt_required
from fs.utils import format_response
from fs.init_db import db
from fs import model
import datetime


class ApiAddStudy(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('rand_num', type=str, location='json', required=True)
        self.reqparser.add_argument('explain', type=str, location='json', required=True)

    @jwt_required()
    def post(self):
        assert current_identity is not None

        args = self.reqparser.parse_args()
        user_id = int(current_identity)
        rand_num = args.get('rand_num', '')
        explain = args.get('explain', '')

        # 根据rand_num查找此课程是否存在
        classes = db.session.query(model.Classes) \
                .filter(model.Classes.rand_num == rand_num) \
                .filter(model.Classes.status == 'normal') \
                .first()
        if classes is None:
            return format_response(-400, '没有查到该课程')

        s = model.Study()
        s.user_id = user_id
        s.classes_id = classes.id
        s.explain = explain
        s.create_time = datetime.datetime.now()
        db.session.add(s)
        db.session.commit()
        return format_response(0, 'success')


class ApiMyStudy(restful.Resource):
    @jwt_required()
    def post(self):
        assert current_identity is not None
        user_id = int(current_identity)
        mystudys = db.session.query(model.Study) \
                .outerjoin(model.Classes, model.Study.classes_id == model.Classes.id) \
                .outerjoin(model.User, model.User.id == user_id) \
                .filter(model.Study.user_id == user_id) \
                .filter(model.Study.status == 'normal') \
                .with_entities(model.User.username,
                               model.Classes.id,
                               model.Classes.name,
                               model.Classes.category,
                               model.Study.explain,
                               model.Study.create_time).all()

        format_studys = []
        for s in mystudys:
            s_item = {}
            s_item['username'] = s[0]
            s_item['classes_id'] = s[1]
            s_item['name'] = s[2]
            s_item['category'] = s[3]
            s_item['explain'] = s[4]
            s_item['create_time'] = s[5].strftime("%Y-%m-%d %H:%M:%S")
            format_studys.append(s_item)
        return format_response(0, 'success', {'mystudys': format_studys})


class ApiStudyResource(restful.Resource):
    @jwt_required()
    def post(self):
        pass
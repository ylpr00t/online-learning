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
                               model.Study.create_time,
                               model.Study.e_coin).all()

        format_studys = []
        for s in mystudys:
            s_item = {}
            s_item['username'] = s[0]
            s_item['classes_id'] = s[1]
            s_item['name'] = s[2]
            s_item['category'] = s[3]
            s_item['explain'] = s[4]
            s_item['create_time'] = s[5].strftime("%Y-%m-%d %H:%M:%S")
            s_item['e_coin'] = s[6]
            format_studys.append(s_item)
        return format_response(0, 'success', {'mystudys': format_studys})


class ApiStudyResource(restful.Resource):
    @jwt_required()
    def post(self):
        pass


class ApiUpdateECoin(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('resource_id', type=int, location='json', required=True) # 查资源的积分
        self.reqparser.add_argument('classes_id', type=int, location='json', required=True) # 和user_id查study_id

    @jwt_required()
    def post(self):
        assert current_identity is not None
        args = self.reqparser.parse_args()
        user_id = int(current_identity)
        classes_id = args.get('classes_id', 0)
        resource_id = args.get('resource_id', 0)
        # 查询资源的积分币
        r = db.session.query(model.Resources) \
            .filter(model.Resources.id == resource_id) \
            .filter(model.Resources.status == 'normal') \
            .first()
        if r is None:
            return format_response(-400, '没有查询到此资源', {})
        e_coin = r.e_coin
        # 查询学习条目，更新e_coin
        s = db.session.query(model.Study) \
            .filter(model.Study.user_id == user_id) \
            .filter(model.Study.classes_id == classes_id) \
            .first()
        if s is None:
            return format_response(-400, '没有查询到次学习', {})
        s.e_coin += e_coin
        # 更新学习追踪
        st = model.StudyTrace()
        st.study_id = s.id
        st.study_ecoin = e_coin
        st.study_info = '%s:查看资源 %s' % (str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), r.name)
        st.status = 'normal'
        db.session.add(st)
        db.session.commit()
        return format_response(0, 'success', {})


class ApiStudyTrace(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('classes_id', type=int, location='json', required=True)

    @jwt_required()
    def post(self):
        assert current_identity is not None
        args = self.reqparser.parse_args()
        user_id = int(current_identity)
        classes_id = args.get('classes_id', 0)
        # 查询study_id
        s = db.session.query(model.Study) \
            .filter(model.Study.user_id == user_id) \
            .filter(model.Study.classes_id == classes_id) \
            .first()
        if s is None:
            return format_response(-400, '没有查询到此学习记录', {})

        # 查询学习追踪
        s_traces = db.session.query(model.StudyTrace) \
            .filter(model.StudyTrace.study_id == s.id) \
            .all()
        format_trace = []
        for s_trace in s_traces:
            item = {}
            item['trace_id'] = s_trace.id
            item['trace_ecoin'] = s_trace.study_ecoin
            item['trace_info'] = s_trace.study_info
            format_trace.append(item)

        #print(format_trace)
        return format_response(0, 'success', {
            'trace_info': format_trace
        })


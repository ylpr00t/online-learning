import flask_restful as restful
from flask_restful import reqparse
from flask_jwt import current_identity, jwt_required
from fs.utils import format_response
from fs.init_db import db
from fs import model
from fs import config
from sqlalchemy import func
import random
import datetime
import csv
import string


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


class ApiDeleteClasses(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('classes_id', type=int, location='json', required=True)
    @jwt_required()
    def post(self):
        assert current_identity is not None
        user_id = int(current_identity)
        args = self.reqparser.parse_args()
        c = db.session.query(model.Classes) \
                .filter(model.Classes.user_id == user_id) \
                .filter(model.Classes.id == args['classes_id']) \
                .filter(model.Classes.status == 'normal') \
                .first()
        if c is None:
            return format_response(-400, '没有查询到此课程', {})
        c.status = 'delete'
        db.session.add(c)
        db.session.commit()
        return format_response(0, 'success', {})


class ApiAddResource(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('classes_id', type=int, location='json', required=True)
        self.reqparser.add_argument('e_coin', type=str, location='json', required=True)
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

        e_coin = int(args.get('e_coin', '0'))
        name = args.get('name', '')
        category = args.get('category', -1)
        desc = args.get('desc', '')
        content = args.get('content', '')
        if name == '' or desc == '' or content == '' or category not in config.RESOURCE_CATEGORY:
            return format_response(-400, '请检查提交的参数')

        r = model.Resources()
        r.classes_id = classes_id
        r.e_coin = e_coin
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

        #s = db.session.query(model.Study) \
        #    .filter(model.Study.user_id == user_id) \
        #    .filter(model.Study.classes_id == classes_id) \
        #    .first()
        #if s is None:
        #    return format_response(-400, '此用户没有添加该课程的学习')

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
            if r.category == 1:
                r_item['category_ch'] = '文本'
            elif r.category == 2:
                r_item['category_ch'] = '图片'
            elif r.category == 3:
                r_item['category_ch'] = '视频'
            else:
                r_item['category_ch'] = '未识别'
            r_item['desc'] = r.desc
            if r.category == 2 or r.category == 3:
                r_item['content'] = 'http://127.0.0.1:8080/' + r.content
            else:
                r_item['content'] = r.content
            r_item['create_time'] = r.create_time.strftime("%Y-%m-%d %H:%M:%S")
            format_resources.append(r_item)
        return format_response(0, 'success', {'myresources': format_resources})


class ApiDeleteResource(restful.Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('resource_id', type=int, location='json', required=True)

    @jwt_required()
    def post(self):
        assert current_identity is not None
        args = self.reqparser.parse_args()
        r = db.session.query(model.Resources) \
                .filter(model.Resources.id == args['resource_id']) \
                .filter(model.Resources.status == 'normal') \
                .first()
        if r is None:
            return format_response(-400, '没有查询到此资料', {})
        r.status = 'delete'
        db.session.add(r)
        db.session.commit()
        return format_response(0, 'success', {})


class ApiMyClassesMem(restful.Resource):
    def __init__(self):
        self.reqarser = reqparse.RequestParser()
        self.reqarser.add_argument('classes_id', type=int, location='json', required=True)

    @jwt_required()
    def post(self):
        assert current_identity is not None
        args = self.reqarser.parse_args()
        classes_id = args.get('classes_id', 0)
        users = db.session.query(model.Study) \
                .filter(model.Study.classes_id == classes_id) \
                .filter(model.Study.status == 'normal') \
                .with_entities(model.Study.user_id, model.Study.e_coin) \
                .all()

        format_users = []
        for user in users:
            item = {}
            user_id = user[0]
            e_coin = user[1]
            user_info = db.session.query(model.User) \
                .outerjoin(model.UserInfo, model.UserInfo.user_id == user_id) \
                .filter(model.User.id == user_id) \
                .filter(model.User.status == 'normal') \
                .with_entities(model.User.username,
                               model.UserInfo.real_name,
                               model.UserInfo.user_email) \
                .first()
            item['user_id'] = user_id
            item['username'] = user_info[0]
            item['realname'] = user_info[1] if user_info[1] else '未定义'
            item['useremail'] = user_info[2] if user_info[2] else '未定义'
            item['e_coin'] = e_coin
            format_users.append(item)

        return format_response(0, 'success', {
            'users': format_users
        })


class ApiExportMemScore(restful.Resource):
    def __init__(self):
        self.reqarser = reqparse.RequestParser()
        self.reqarser.add_argument('classes_id', type=int, location='json', required=True)
        self.reqarser.add_argument('sum_score', type=int, location='json', required=True)
        self.reqarser.add_argument('five_level', type=int, location='json', required=True)

    def generate_file_name(self, filename):
        random_str =  ''.join(random.sample(string.ascii_letters+string.digits, 32))
        random_str = random_str + '.' + filename.split('.')[1]
        return random_str

    def get_level(self, score):
        if 90 <= score <= 100:
            return 'A'
        elif 70 <= score < 90:
            return 'B'
        elif 60 <= score < 70:
            return 'C'
        elif 30 <= score < 60:
            return 'D'
        elif 0 <= score <30:
            return 'E'
        else:
            return 'ERROR'

    @jwt_required()
    def post(self):
        assert current_identity is not None
        args = self.reqarser.parse_args()
        classes_id = args.get('classes_id', 0)
        sum_score = args.get('sum_score', 100)
        five_level = args.get('five_level', 0)

        # 查询所有用户
        users = db.session.query(model.Study) \
                .filter(model.Study.classes_id == classes_id) \
                .filter(model.Study.status == 'normal') \
                .with_entities(model.Study.user_id, model.Study.e_coin) \
                .all()

        # 查询该课程总的E_COIN
        e_coin_sum = db.session.query(func.sum(model.Resources.e_coin)).filter(model.Resources.classes_id == classes_id).scalar()

        # 查询每个用户的具体信息
        csv_headers = ['ID', 'USERNAME', 'REALNAME', 'ECOIN', 'SCORE']
        if five_level == 1:
            csv_headers.append('LEVEL')

        csv_rows = []
        data_id = 1
        for user in users:
            item = {}
            user_id = user[0]
            e_coin = user[1]
            user_info = db.session.query(model.User) \
                .outerjoin(model.UserInfo, model.UserInfo.user_id == user_id) \
                .filter(model.User.id == user_id) \
                .filter(model.User.status == 'normal') \
                .with_entities(model.User.username, model.UserInfo.real_name) \
                .first()
            item['ID'] = data_id
            item['USERNAME'] = user_info[0]
            item['REALNAME'] = user_info[1] if user_info[1] else '未定义'
            item['REALNAME'] = item['REALNAME'].encode('utf-8')
            item['ECOIN'] = e_coin
            item['SCORE'] = str(round(e_coin / e_coin_sum, 2) * sum_score)
            if five_level == 1:
                item['LEVEL'] = self.get_level(float(item['SCORE']))
            csv_rows.append(item)
            data_id += 1

        filename = self.generate_file_name('.csv')
        csv_filename ='./etc/csv/' + filename
        with open(csv_filename, 'w') as f:
            f_csv = csv.DictWriter(f, csv_headers)
            f_csv.writeheader()
            f_csv.writerows(csv_rows)

        return format_response(0, 'success', {
            'filename': filename
        })






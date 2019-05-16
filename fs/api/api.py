from flask_restful import Api


def bind_app(app):
    api = Api(app)

    from . import welcome
    api.add_resource(welcome.Index, '/api/welcome')
    api.add_resource(welcome.ApiIsLogin, '/api/islogin')

    from . import user
    api.add_resource(user.ApiRegister, '/api/register')
    api.add_resource(user.ApiLogin, '/api/login')
    api.add_resource(user.ApiUserList, '/api/userlist')
    api.add_resource(user.ApiIsAdmin, '/api/is_admin')
    api.add_resource(user.ApiSuperSwitch, '/api/super_switch')

    from . import classes
    api.add_resource(classes.ApiAddClasses, '/api/addclasses')
    api.add_resource(classes.ApiMyClass, '/api/myclasses')
    api.add_resource(classes.ApiAddResource, '/api/addresource')
    api.add_resource(classes.ApiMyResources, '/api/myresources')
    api.add_resource(classes.ApiDeleteClasses, '/api/deleteclasses')
    api.add_resource(classes.ApiDeleteResource, '/api/deleteresource')

    from . import study
    api.add_resource(study.ApiMyStudy, '/api/mystudy')
    api.add_resource(study.ApiAddStudy, '/api/addstudy')
    api.add_resource(study.ApiStudyResource, '/api/studyresource')

    from . import setting
    api.add_resource(setting.ApiSetting, '/api/setting')

    from . import myinfo
    api.add_resource(myinfo.ApiMyInfo, '/api/myinfo')

    from . import upload
    api.add_resource(upload.ApiUpload, '/api/upload')
from flask_restful import Api


def bind_app(app):
    api = Api(app)

    from . import welcome
    api.add_resource(welcome.Index, '/api/welcome')

    from . import user
    api.add_resource(user.ApiRegister, '/api/register')
    api.add_resource(user.ApiLogin, '/api/login')
    api.add_resource(user.ApiUserList, '/api/userlist')
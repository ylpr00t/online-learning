import flask_restful as restful


class Index(restful.Resource):
    def get(self):
        return 'welcome to ylp restful'

from flask import request
import random
import string
import flask_restful as restful
from fs.utils import format_response


class ApiUpload(restful.Resource):
    def check_file_type(self, filename):
        return True

    def generate_file_name(self, filename):
        random_str =  ''.join(random.sample(string.ascii_letters+string.digits, 32))
        random_str = random_str + '.' + filename.split('.')[1]
        return random_str

    def post(self):
        file = request.files['file']
        res_type = int(request.form['resource_type']) # str
        if not file:
            return format_response(-400, 'file is None', {})
        if self.check_file_type(file.filename) == False:
            return format_response(-400, 'file type error', {})

        file_name = self.generate_file_name(file.filename)
        if res_type == 2:
            file.save('./etc/img/' + file_name)
        elif res_type == 3:
            file.save('./etc/video/' + file_name)
        else:
            return format_response(-400, 'unknown file type', {})

        return format_response(0, 'success', {
            'filename': str(file_name)
        })
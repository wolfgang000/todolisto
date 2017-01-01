# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import os
from flask import Flask , render_template, url_for
from flask_restful import reqparse, abort, Api, Resource


if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/') :
	#GAE Production config
	app = Flask(__name__)
	app.debug = False
else :
	#Dev config
	app = Flask(__name__, static_folder='frontend/dist')
	app.debug = True


api = Api(app)


@app.route('/')
def index():
    return app.send_static_file('index.html ')



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


class TaskDetail(Resource):
    def get(self, id):
		return "",200

    def delete(self, id):
		pass

    def put(self, id):
		pass

class TaskList(Resource):
    def get(self):
        return "",200

    def post(self):
		pass

api.add_resource(TaskList, '/tasks/', endpoint='task-list')
api.add_resource(TaskDetail, '/tasks/<id>', endpoint='task-detail')




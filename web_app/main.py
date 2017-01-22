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
from core import entities
import os
from flask import Flask , render_template, url_for, request
from flask_restful import reqparse, abort, Api, Resource



#Config
from enum import Enum

class DatabaseType(Enum):
	GAE_NOSQL = 1

db_type = DatabaseType.GAE_NOSQL

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
	#GAE Production config
	app = Flask(__name__, static_folder='static', template_folder='templates', )
	app.debug = False

elif os.getenv('SERVER_SOFTWARE', '').startswith('Development/'):
	#GAE Develop config
	import sys
	import argparse
	app = Flask(__name__, static_folder='static', template_folder='templates', )
	app.debug = True

else:
	#Dev config
	app = Flask(__name__, static_folder='static', template_folder='templates',)
	app.debug = True

if db_type == DatabaseType.GAE_NOSQL:
	from db.gae import no_sql
	repository = no_sql.Repository()
#
import web_app.serializers

api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


class TaskDetail(Resource):
	def get(self, id):
		task = repository.task.get(id)
		if task == None:
			return "", 404

		task_serialiers =  web_app.serializers.TaskSchema()
		task_json, errors = task_serialiers.dumps(task)

		return task_json,200

	def delete(self, id):
		task = repository.task.get(id)
		if task == None:
			return "", 404
		repository.task.delete(task)
		return "",200

	def put(self, id):
		task = repository.task.get(id)
		if task == None:
			return "", 404
		
		task_serialiers =  web_app.serializers.TaskSchema()
		task_request , errors = task_serialiers.loads(request.data)
		if errors != {} :
			return errors , 400	

		task.title = task_request['title']
		response = repository.task.update(task)
		task_json, errors = task_serialiers.dumps(response)
		if errors != {}:
			return errors , 500	

		return task_json,201

class TaskList(Resource):
	def get(self):
		tasks = repository.task.get_all()
		task_serialiers =  web_app.serializers.TaskSchema()
		
		task_json, errors = task_serialiers.dumps(tasks,many=True)
		return task_json,200

	def post(self):
		task_serialiers =  web_app.serializers.TaskSchema()
		task_request , errors = task_serialiers.loads(request.data)
		if errors != {} :
			return errors , 400	
		
		task_entity = entities.Task()
		task_entity.title = task_request['title']
		response = repository.task.add(task_entity)

		task_json, errors = task_serialiers.dumps(response)
		if errors != {}:
			return errors , 500	

		return task_json,201

api.add_resource(TaskList, '/tasks/', endpoint='task-list')
api.add_resource(TaskDetail, '/tasks/<id>', endpoint='task-detail')




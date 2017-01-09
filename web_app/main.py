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

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/') :
	#GAE Production config
	app = Flask(__name__,static_folder='static', template_folder='templates', )
	app.debug = False

elif os.getenv('SERVER_SOFTWARE', '').startswith('Development/') :
	#GAE Develop config
	import sys
	import argparse
	app = Flask(__name__,static_folder='static', template_folder='templates', )
	app.debug = True
	try:
		GAE_HOME = None
		GAE_HOME = os.environ['GAE_HOME']

		def fixup_paths(path):
			"""
			Adds GAE SDK path to system path and appends it to the google path
			if that already exists.
			"""
			# Not all Google packages are inside namespace packages, which means
			# there might be another non-namespace package named `google` already on
			# the path and simply appending the App Engine SDK to the path will not
			# work since the other package will get discovered and used first.
			# This emulates namespace packages by first searching if a `google` package
			# exists by importing it, and if so appending to its module search path.
			try:
				import google
				google.__path__.append("{0}/google".format(path))
			except ImportError:
				pass
			sys.path.insert(0, path)

		parser = argparse.ArgumentParser(
			description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter)
		parser.add_argument(
			'sdk_path',
			help='The path to the Google App Engine SDK or the Google Cloud SDK.')
		parser.add_argument(
			'--test-path',
			help='The path to look for tests, defaults to the current directory.',
			default=os.getcwd())
		parser.add_argument(
			'--test-pattern',
			help='The file pattern for test modules, defaults to *_test.py.',
			default='*_test.py')


		# If the SDK path points to a Google Cloud SDK installation
		# then we should alter it to point to the GAE platform location.
		if os.path.exists(os.path.join(GAE_HOME, 'platform/google_appengine')):
			GAE_HOME = os.path.join(GAE_HOME, 'platform/google_appengine')


		# Make sure google.appengine.* modules are importable.
		fixup_paths(GAE_HOME)

		# Make sure all bundled third-party packages are available.
		import dev_appserver
		dev_appserver.fix_sys_path()

		# Loading appengine_config from the current project ensures that any
		# changes to configuration there are available to all tests (e.g.
		# sys.path modifications, namespaces, etc.)
		try:
			import appengine_config
			(appengine_config)
		except ImportError:
			print('Note: unable to import appengine_config.')


	except KeyError:
			pass


else :
	#Dev config
	app = Flask(__name__, static_folder='frontend/dist', template_folder='frontend/dist',)
	app.debug = True
	if db_type == DatabaseType.GAE_NOSQL:
		import sys
		import argparse
		try:
			GAE_HOME = None
			GAE_HOME = os.environ['GAE_HOME']

			def fixup_paths(path):
				"""
				Adds GAE SDK path to system path and appends it to the google path
				if that already exists.
				"""
				# Not all Google packages are inside namespace packages, which means
				# there might be another non-namespace package named `google` already on
				# the path and simply appending the App Engine SDK to the path will not
				# work since the other package will get discovered and used first.
				# This emulates namespace packages by first searching if a `google` package
				# exists by importing it, and if so appending to its module search path.
				try:
					import google
					google.__path__.append("{0}/google".format(path))
				except ImportError:
					pass
				sys.path.insert(0, path)

			parser = argparse.ArgumentParser(
				description=__doc__,
				formatter_class=argparse.RawDescriptionHelpFormatter)
			parser.add_argument(
				'sdk_path',
				help='The path to the Google App Engine SDK or the Google Cloud SDK.')
			parser.add_argument(
				'--test-path',
				help='The path to look for tests, defaults to the current directory.',
				default=os.getcwd())
			parser.add_argument(
				'--test-pattern',
				help='The file pattern for test modules, defaults to *_test.py.',
				default='*_test.py')


			# If the SDK path points to a Google Cloud SDK installation
			# then we should alter it to point to the GAE platform location.
			if os.path.exists(os.path.join(GAE_HOME, 'platform/google_appengine')):
				GAE_HOME = os.path.join(GAE_HOME, 'platform/google_appengine')


			# Make sure google.appengine.* modules are importable.
			fixup_paths(GAE_HOME)

			# Make sure all bundled third-party packages are available.
			import dev_appserver
			dev_appserver.fix_sys_path()

			# Loading appengine_config from the current project ensures that any
			# changes to configuration there are available to all tests (e.g.
			# sys.path modifications, namespaces, etc.)
			try:
				import appengine_config
				(appengine_config)
			except ImportError:
				print('Note: unable to import appengine_config.')


		except KeyError:
				pass

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
		return "",200

	def delete(self, id):
		pass

	def put(self, id):
		pass

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




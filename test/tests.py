import os
from web_app import main
import web_app
import unittest
import tempfile
import json
from unidecode import unidecode
from google.appengine.ext import testbed

class FuncionalRestSevicesTestCase(unittest.TestCase):
	
	def setUp(self):
		main.app.testing = True
		self.app = main.app.test_client()
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Then activate the testbed, which will allow you to use
		# service stubs.
		self.testbed.activate()
		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		self.task_serialiers =  web_app.serializers.TaskSchema()


	def tearDown(self):
		# Don't forget to deactivate the testbed after the tests are
		# completed. If the testbed is not deactivated, the original
		# stubs will not be restored.
		self.testbed.deactivate()
	
	def test_task_list(self):
		with main.app.test_request_context():
			url = main.url_for('task-list')
			r = self.app.get(url)
			self.assertEqual(r.status_code, 200)
			self.assertEqual(r.data, '"[]"\n')

			example_request_task = '{"title":"New_title"}'
			r = self.app.post(url, data = example_request_task )
			self.assertEqual(r.status_code, 201)
			self.task_serialiers =  web_app.serializers.TaskSchema()
			task_obj = self.task_serialiers.loads(json.loads(r.data))
			self.assertDictEqual(task_obj.errors, {} )
			self.assertIsNotNone(task_obj.data['id'])
			self.assertIsNotNone(task_obj.data['title'])
			self.assertIsNotNone(task_obj.data['created_at'])

			example_bad_request_task = '{"title1":"New_title"}'
			r = self.app.post(url, data = example_bad_request_task )
			self.assertEqual(r.status_code, 400)
		
	def test_task_CRUD(self):
		with main.app.test_request_context():
			url_list = main.url_for('task-list')
			#url_detail = main.url_for('task-detail')

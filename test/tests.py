import os
from web_app import main
import web_app
import unittest
import tempfile
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
			data, errors = self.task_serialiers.loads(str(r.data))
			print r.data
			print 'data2',data
			print 'errors',errors
			self.assertIsNotNone(data.id)

			example_bad_request_task = '{"title1":"New_title"}'
			r = self.app.post(url, data = example_bad_request_task )
			self.assertEqual(r.status_code, 400)

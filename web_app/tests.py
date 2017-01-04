import os
from web_app import main
import web_app.serializers
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):

	def setUp(self):
		main.app.testing = True
		self.app = main.app.test_client()
	
	def test_web_server(self):
		r = self.app.get('/')
		self.assertEqual(r.status_code, 200)

class FlaskTestCase(unittest.TestCase):
	
	def test_task_serializer(self):
		web_app.serializers.TaskSchema({'title':'Alfon','id':4})
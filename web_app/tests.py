import os
from web_app import main
import web_app.serializers
from core import entities 
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):

	def setUp(self):
		main.app.testing = True
		self.app = main.app.test_client()
	
	def test_web_server(self):
		r = self.app.get('/')
		self.assertEqual(r.status_code, 200)

class SerializersTestCase(unittest.TestCase):

	def setUp(self):
		self.task_serialiers =  web_app.serializers.TaskSchema()
	
	def test_task_serializer(self):
		task_dict ={'title':'Alfon','id':4}
		task_serializaer = self.task_serialiers.dumps(task_dict)
		#self.assertDictEqual(task_dict,task_serializaer.data)

	def test_serialze_entity(self):
		task_entity = entities.Task(id=1, title='Alfonso')
		task_serializaer = self.task_serialiers.dumps(task_entity)
		self.assertIsNotNone(task_serializaer.data)
		self.assertGreater(len(task_serializaer.data),10)

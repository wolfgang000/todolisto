import os
from web_app import main
import web_app.serializers
import simplejson 
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
		task_json, errors = self.task_serialiers.dumps(task_entity)
		self.assertEqual(errors,{})
		self.assertEqual(task_json,'{"id": 1, "title": "Alfonso"}')
	
	def test_serialze_from_json(self):
		example_task = {"id" : 1, "title":"Alfonso" }
		task_json = simplejson.dumps( example_task )
		self.task_serialiers =  web_app.serializers.TaskSchema()
		data, errors = self.task_serialiers.loads(task_json)
		self.assertDictEqual(errors,{})
		self.assertDictEqual(data,example_task)

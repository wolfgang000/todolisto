from unittest import TestCase
from core.entities import Task

class TrackTests(TestCase):

	def test_none_instantiation(self):
		task = Task()
		self.assertEqual(task,Task())
	
	def test_data_instantiation(self):
		task = Task(id = 1, title='Title', description='text')
		self.assertEqual(task.id,1)
		self.assertEqual(task.title,'Title')
		self.assertEqual(task.description,'text')


from unittest import TestCase
from core.entities import Task , Status
from core.repositories import TaskBaseRepository

class TrackTests(TestCase):

	def test_none_instantiation(self):
		task = Task()
		self.assertEqual(task,Task())
	
	def test_data_instantiation(self):
		task = Task(id = 1, title='Title', description='text')
		self.assertEqual(task.id,1)
		self.assertEqual(task.title,'Title')
		self.assertEqual(task.description,'text')
		self.assertEqual(task._status, Status.ADDED)

class TaskAbstractRepositoryTests(TestCase):

	def test_abstract_instantiation(self):
		with self.assertRaises(Exception) as context:
			TaskBaseRepository()
		self.assertTrue('Can\'t instantiate abstract class' in str(context.exception))
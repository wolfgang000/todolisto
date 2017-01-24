from unittest import TestCase
import datetime
from core.entities import Task , Status
from core.repositories import TaskBaseRepository

class TrackTests(TestCase):

	def test_none_instantiation(self):
		now = datetime.datetime.utcnow()
		task = Task(created_at = now)
		self.assertEqual(task,Task(created_at = now))
	
	def test_data_instantiation(self):
		task = Task(id = 1, title='Title', )
		self.assertEqual(task.id,1)
		self.assertEqual(task.title,'Title')
		self.assertAlmostEqual(task.created_at, datetime.datetime.utcnow(),delta = datetime.timedelta(seconds=1) )
		self.assertEqual(task._status, Status.ADDED)

class TaskAbstractRepositoryTests(TestCase):

	def test_abstract_instantiation(self):
		with self.assertRaises(Exception) as context:
			TaskBaseRepository()
		self.assertTrue('Can\'t instantiate abstract class' in str(context.exception))
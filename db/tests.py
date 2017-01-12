import unittest
import os
import sys
import argparse

from core.entities import Task
from core.entities import Status
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

	from db.gae import no_sql
	from google.appengine.ext import testbed


except KeyError:
        pass

@unittest.skipIf(GAE_HOME == None, "GAE_HOME not define")
class GaeRepositoriesTests(unittest.TestCase):

	def setUp(self):
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Then activate the testbed, which will allow you to use
		# service stubs.
		self.testbed.activate()
		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

	def tearDown(self):
		# Don't forget to deactivate the testbed after the tests are
		# completed. If the testbed is not deactivated, the original
		# stubs will not be restored.
		self.testbed.deactivate()

	def test_create_and_retrieve_task(self):
		task_repo = no_sql.TaskRepository()
		
		task_intance = task_repo.add(Task(title = 'Title',))
		self.assertIsNotNone(task_intance.id)
		
		task_new_intance = task_repo.get(task_intance.id)

		self.assertEqual(task_intance.id,task_new_intance.id)
		self.assertEqual(task_intance.title ,task_new_intance.title)
	
	def test_get_all_tasks(self):
		task_repo = no_sql.TaskRepository()
		task_repo.add(Task(title = 'Title1',))
		task_repo.add(Task(title = 'Title2',))
		task_repo.add(Task(title = 'Title3',))

		self.assertEqual(len(task_repo.get_all()), 3)
	
	def test_get_nonexistent_entry(self):
		task_repo = no_sql.TaskRepository()
		task = task_repo.get(122)
		self.assertIsNone(task)
	
	def test_full_CRUD_process(self):
		task_repo = no_sql.TaskRepository()
		
		t = Task(title = 'Title',)
		self.assertEqual(t._status,Status.ADDED)
		
		task_intance = task_repo.add(t)
		self.assertEqual(task_intance._status,Status.UNCHANGE)
		
		task_intance.title = 'New Title'
		self.assertEqual(task_intance._status,Status.MODIFIED)
		
		task_intance_with_update = task_repo.update(task_intance)
		self.assertEqual(task_intance_with_update._status,Status.UNCHANGE)
		self.assertEqual(task_intance_with_update.title, 'New Title')

		task_instance_with_get = task_repo.get(task_intance_with_update.id)
		self.assertEqual(task_intance_with_update.id, task_instance_with_get.id)
		self.assertEqual(task_intance_with_update.title, task_instance_with_get.title)
		self.assertEqual(task_intance_with_update._status, task_instance_with_get._status)
		
		task_repo.delete(task_instance_with_get)
		task_instance = task_repo.get(task_intance_with_update.id)
		self.assertIsNone(task_instance)


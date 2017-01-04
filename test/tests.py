import os
from web_app import main
import unittest
import tempfile

class FuncionalRestSevicesTestCase(unittest.TestCase):

	def setUp(self):
		main.app.testing = True
		self.app = main.app.test_client()
	
	def test_task_list(self):
		with main.app.test_request_context():
			url = main.url_for('task-list')
			r = self.app.get(url)
			self.assertEqual(r.status_code, 200)
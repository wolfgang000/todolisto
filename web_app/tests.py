import os
from web_app import main
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):

	def setUp(self):
		main.app.testing = True
		self.app = main.app.test_client()
	
	def test_web_server(self):
		r = self.app.get('/')
		self.assertEqual(r.status_code, 200)

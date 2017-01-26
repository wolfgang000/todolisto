import nose2
import os
import sys
import argparse
import config
try:
	config.GAE_HOME = None
	config.GAE_HOME = os.environ['GAE_HOME']

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
	if os.path.exists(os.path.join(config.GAE_HOME, 'platform/google_appengine')):
		config.GAE_HOME = os.path.join(config.GAE_HOME, 'platform/google_appengine')


	# Make sure google.appengine.* modules are importable.
	fixup_paths(config.GAE_HOME)

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

except KeyError:
        pass

if __name__ == '__main__':
  nose2.discover()
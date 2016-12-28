import abc
from . import entities

class TaskBaseRepository(abc.ABCMeta('ABC', (object,), {})):

	@abc.abstractmethod
	def get(self, id):
		pass

	@abc.abstractmethod
	def add(self, obj):
		pass

	@abc.abstractmethod
	def update(self, obj):
		pass 

	@abc.abstractmethod
	def delete(self, obj):
		pass
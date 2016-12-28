from abc import ABCMeta, abstractmethod
from . import entities

class TaskBaseRepository(object, metaclass=ABCMeta):

	@abstractmethod
	def get(self, id):
		pass

	@abstractmethod
	def add(self, obj):
		pass

	@abstractmethod
	def update(self, obj):
		pass 

	@abstractmethod
	def delete(self, obj):
		pass
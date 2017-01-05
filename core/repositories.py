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
	


class Repository(abc.ABCMeta('ABC', (object,), {})):

	def __get_user_repo(self):
		return self.__user_repo
	user = property(__get_user_repo,)

	def __get_task_repo(self):
		return self.__task_repo
	task = property( __get_task_repo,)
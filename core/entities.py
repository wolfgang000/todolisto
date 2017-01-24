from enum import Enum
import datetime

class Status(Enum):
	UNCHANGE = 1 
	MODIFIED = 2
	ADDED = 3
	DELETE = 4

class Base(object):
	def __init__(self):
		self._status = Status.ADDED

	
class Task(Base):
	def __init__(self, id = None, title=None, created_at = None):
		super(Task, self).__init__()
		self.__set_id(id)
		self.__set_title(title)
		if created_at == None: 
			self.__set_created_at(datetime.datetime.utcnow())
		else:
			self.__set_created_at(created_at)

	def __get_id(self):
		return self.__id

	def __set_id(self, id):
		self.__id = id
	id = property(__get_id, __set_id)

	def __get_title(self):
		return self.__title
	def __set_title(self, title):
		if self._status == Status.UNCHANGE:
			self._status = Status.MODIFIED
		self.__title = title
	title = property(__get_title, __set_title)

	def __get_created_at(self):
		return self.__created_at

	def __set_created_at(self, created_at):
		if self._status == Status.UNCHANGE:
			self._status = Status.MODIFIED
		self.__created_at = created_at

	created_at = property(__get_created_at, __set_created_at)


	def __eq__(self, other):
		
		comparation = (
			self.id == other.id
			and self.title == other.title
			#  and self.created_at == other.title 
		)
		return comparation
	
	def __str__(self):
		return str(self.__dict__)

class List:
	def __init__(self, id = None, title=None, description=None,):
		self.__set_id(id)
		self.__set_title(title)
		self.__set_description(description)
	
	def add_task(self, task):
		task.list = self
		self.__tasks.add(task)
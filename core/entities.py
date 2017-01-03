from enum import Enum

class Status(Enum):
	UNCHANGE = 1 
	MODIFIED = 2
	ADDED = 3
	DELETE = 4

class Base:
	def __init__(self):
		self.__status = Status.ADDED

class Task(Base):
	def __init__(self, id = None, title=None, description=None,):
		Base.__init__(self)
		self.__set_id(id)
		self.__set_title(title)
		self.__set_description(description)

	def __get_id(self):
		return self.__id
	def __set_id(self, id):
		self.__id = id
	id = property(__get_id, __set_id)

	def __get_title(self):
		return self.__title
	def __set_title(self, title):
		self.__title = title
	title = property(__get_title, __set_title)

	def __get_description(self):
		return self.__description
	def __set_description(self, description):
		self.__description = description
	description = property(__get_description, __set_description)

	def __eq__(self, other):
		return self.__dict__ == other.__dict__
	
	def __str__(self):
		return str(self.__dict__)
class Task:
	def __init__(self, id = None, title=None, description=None, ):
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

class List:
	def __init__(self, id = None, title=None, description=None,):
		self.__set_id(id)
		self.__set_title(title)
		self.__set_description(description)
	
	def add_task(self, task)
		task.list = self
		self.__tasks.add(task)
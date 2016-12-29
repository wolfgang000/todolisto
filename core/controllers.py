from . import entities

class Controller:
	def __init__(self, repository):
		self.__repository_ = repository 
	
	def add_task(self, task):
		new_task = self.__repositor.add(task)
		return new_task
	
	def get_task(self, task):
		pass
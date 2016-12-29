from . import entities

class Controller:
	def __init__(self, repository):
		self.__repository = repository 
	
	def add_task(self, task):
		new_task = self.__repositor.add(task)
		return new_task
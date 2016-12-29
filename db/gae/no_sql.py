from core import repositories
from core import entities

from google.appengine.ext import ndb

class Task(ndb.Model):
	title = ndb.StringProperty()
	description = ndb.StringProperty()

class TaskRepository(repositories.TaskBaseRepository):
	def get(self, id):
		task = entities.Task()
		db_task = Task(id = id)
		
		task.id = id
		task.title = db_task.title
		task.description = db_task.description
		
		return task
	
	def add(self, obj):
		db_task = Task(title = obj.title, description = obj.description)
		id = db_task.put().id()
		obj.id = id
		return obj

	def update(self, obj):
		pass 

	def delete(self, obj):
		pass

class Repository(repositories.Repository):
	pass
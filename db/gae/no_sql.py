from core import repositories
from core import entities

from google.appengine.ext import ndb

class Task(ndb.Model):
	title = ndb.StringProperty()

class TaskRepository(repositories.TaskBaseRepository):
	def get(self, id):
		task = entities.Task()
		db_task = Task.get_by_id(id)
		task = self.mapper_db_entity(db_task)
		task._status = entities.Status.UNCHANGE
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
	
	def mapper_db_entity(self, db):
		task = entities.Task()
		task.id = db.id
		task.title = db.title
		return task


class Repository(repositories.Repository):
	pass
from core import repositories
from core import entities

from google.appengine.ext import ndb

class Task(ndb.Model):
	title = ndb.StringProperty()
	description = ndb.StringProperty()

class TaskRepository(repositories.TaskBaseRepository):
	def get(self, id):
		track = entities.Track()
		db_task = Task(id = id)
		
		track.id = id
		track.title = db_task.title
		track.description = db_task.description
		
		return track
	
	def add(self, obj):
		db_track = Track(title = obj.title, description = obj.description)
		id = db_track.put().id()
		obj.id = id
		return id

	def update(self, obj):
		pass 

	def delete(self, obj):
		pass

class Repository(repositories.Repository):
	pass
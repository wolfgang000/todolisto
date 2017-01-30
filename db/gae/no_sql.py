from core import repositories
from core import entities
from google.appengine.ext import ndb
import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()


class Task(ndb.Model):
	title = ndb.StringProperty()
	created_at = ndb.DateTimeProperty()
	created_by = ndb.StringProperty()

class TaskRepository(repositories.TaskBaseRepository):
	def get(self, id):
		task = entities.Task()
		db_task = Task.get_by_id(id)
		if db_task != None: 
			task = self.mapper_db_entity(db_task)
			task._status = entities.Status.UNCHANGE
			return task
		else :
			return None
	
	def add(self, obj):
		db_task = Task(title = obj.title, created_at = obj.created_at,created_by = obj.user.id)
		id = db_task.put().id()
		obj.id = id
		obj._status = entities.Status.UNCHANGE
		return obj

	def update(self, obj):
		if obj._status == entities.Status.MODIFIED:
			db_task = Task.get_by_id(obj.id)
			if db_task == None:
				raise 'Task entity with id ' + obj.id + ' not found in db'
			db_task.title = obj.title
			db_task.created_at = obj.created_at
			db_task = db_task.put()
			if db_task == None:
				raise 'Task entity with id ' + obj.id + ' not is not able to update in db'
			obj._status = entities.Status.UNCHANGE
			return obj
		else:
			return obj
		

	def delete(self, obj):
		db_task = Task.get_by_id(obj.id)
		if db_task == None:
			raise 'Task entity with id ' + obj.id + ' not found in db'
		db_task.key.delete()
	def delete_by_id(self, id):
		db_task = Task.get_by_id(id)
		if db_task == None:
			raise Exception('Task entity with id ' + id + ' not found in db')
		db_task.key.delete()
	
	def get_all(self):
		tasks_db = Task.query()
		tasks = []
		for task_db in tasks_db:
			tasks.append(self.mapper_db_entity(task_db))
		
		return tasks
	
	def get_all_by_user(self,user):
		tasks_db = Task.query(Task.created_by == user.id)
		tasks = []
		for task_db in tasks_db:
			tasks.append(self.mapper_db_entity(task_db))
		
		return tasks


	def mapper_db_entity(self, db):
		task = entities.Task()
		task.id = db.key.id()
		task.title = db.title
		task.created_at = db.created_at
		task.created_by = db.created_by
		return task


class UserRepository():
	def get_by_token(self, token):
		claims = google.oauth2.id_token.verify_firebase_token(token, HTTP_REQUEST)
		if not claims:
			return None
		id = claims['sub']
		name = claims.get('sub', None)
		email = claims.get('email', None)
		return entities.User(id=id,name=name,email=email)


class Repository(repositories.Repository):
	
	def __init__(self):
		self.__task_repo =  TaskRepository()
		self.__user_repo = UserRepository()


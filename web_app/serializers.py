from marshmallow import Schema, fields, pprint

class TaskSchema(Schema):
	title = fields.Str()
	id = fields.Int()
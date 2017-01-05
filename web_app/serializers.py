from marshmallow import Schema, fields, pprint

class TaskSchema(Schema):
	name = fields.Str()
	id = fields.Int()
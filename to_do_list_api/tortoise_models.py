from tortoise.models import Model
from tortoise import fields

class ToDo(Model):
    id = fields.IntField(pk = True)
    title = fields.TextField()
    description = fields.TextField(null=True)
    def __str__(self):
        return self.title
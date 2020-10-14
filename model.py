from peewee import *

db = SqliteDatabase('users.db')


class User(Model):
    id = IntegerField()
    department_name = CharField()
    group_number = CharField()
    subgroup = IntegerField()

    class Meta:
        database = db

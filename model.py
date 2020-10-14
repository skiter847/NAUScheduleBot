from peewee import *

db = SqliteDatabase('users.db')


class User(Model):
    id = IntegerField()
    department_name = CharField()
    group_number = CharField()
    subgroup = IntegerField()
    subscribe = BooleanField(default=False)

    class Meta:
        database = db


def init_db():
    if not db.is_closed():
        db.create_tables([User], safe=True)

from peewee import *
import sqlite3

db = SqliteDatabase('users.db')

class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = IntegerField(unique=True)
    ref = IntegerField(default=0)

    @classmethod
    async def get_user(cls, user_id):
        return cls.get(user_id == user_id)

    @classmethod
    async def get_ref_count(cls, user_id):
        return cls.get(Users.user_id == user_id).ref

    @classmethod
    async def increase_ref_count(cls, user_id):
        user = cls.get_user(user_id)
        user.ref += 1
        user.save

    @classmethod
    async def user_exists(cls, user_id):
        query = cls().select().where(cls.user_id == user_id)
        return query.exists()

    @classmethod
    async def create_user(cls, user_id):
        user, created = cls.get_or_create(user_id=user_id)

db.create_tables([Users])
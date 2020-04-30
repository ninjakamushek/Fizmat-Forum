import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Action(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'statistics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    thread_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("threads.id"))
    liked = sqlalchemy.Column(sqlalchemy.Boolean)
    viewed = sqlalchemy.Column(sqlalchemy.Boolean)
    user = orm.relation('User')
    thread = orm.relation('Thread')

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'answers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    thread_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("threads.id"))
    comm_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("comments.id"))
    user = orm.relation('User')
    thread = orm.relation('Thread')
    comment = orm.relation('Comment')

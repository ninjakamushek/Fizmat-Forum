import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .categories import association_table
from .db_session import SqlAlchemyBase


class Thread(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'threads'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    like_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    view_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    comment_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user = orm.relation('User')
    categories = orm.relation("Category", secondary=association_table, backref="threads")

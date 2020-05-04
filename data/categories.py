import sqlalchemy

from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table('association', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('threads', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('threads.id')),
                                     sqlalchemy.Column('categories', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('categories.id')))


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

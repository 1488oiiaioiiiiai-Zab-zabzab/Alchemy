import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class News_C(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    content = sa.Column(sa.String, nullable=True)
    created_date = sa.Column(sa.DateTime, default=dt.datetime.now)
    is_private = sa.Column(sa.Boolean, default=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id")) # table.column
    user_orm_rel = orm.relationship('User_C') # class
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class DepartmentC(SqlAlchemyBase):
    __tablename__ = "table_department"
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("table_users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    users_orm_rel = orm.relationship("UserC")

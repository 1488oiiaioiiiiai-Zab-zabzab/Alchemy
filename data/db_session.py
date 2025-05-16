import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()  # Некоторая абстрактная база
# В неё будем наследовать модели

__factory = None  # для получения сессий подключения к нашей базе данных.


def global_init(db_address):
    global __factory

    if __factory:
        return

    if not db_address or not db_address.strip():
        raise Exception("Необходимо указать имя базы данных")

    connect_str = f"sqlite:///{db_address.strip()}?check_same_thread=False"
    print(f"Подключение к базе данных по адресу {connect_str}")

    engine = sa.create_engine(connect_str, echo=False)  # Алхимия делает движок
    __factory = orm.sessionmaker(bind=engine)  # создаёи сессию
    print("Ссесия создана", __factory)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()

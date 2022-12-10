from models import Appeals, Base
import database
from sqlalchemy.orm import Session
import re

Base.metadata.create_all(bind=database.engine)


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def message_decode(message):
    """Декодирование сообщения."""
    data_list = message.decode().split(',')
    data_parse = re.sub(r"[ ()-]", "", data_list[3])
    data_list[3] = data_parse
    return create(next(get_db()), data_list)


def create(db, data_list):
    """Запись сообщения в БД postgres."""
    new_appeal = Appeals(
        first_name=data_list[0],
        last_name=data_list[1],
        middle_name=data_list[2],
        phone_number=int(data_list[3]),
        appeal=data_list[4]
    )
    db.add(new_appeal)
    db.commit()
    db.refresh(new_appeal)

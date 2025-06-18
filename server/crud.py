from sqlalchemy.orm import Session
from server.models import Record
from server.schemas import RecordCreate


def create_record(db: Session, record_data: RecordCreate) -> Record:
    """Создаёт и сохраняет новую запись в базе данных из объекта Pydantic."""

    record = Record(**record_data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_records(db: Session, skip: int = 0, limit: int = 10) -> list[Record]:
    """Возвращает список записей с учётом пагинации (skip и limit)."""

    return db.query(Record).offset(skip).limit(limit).all()
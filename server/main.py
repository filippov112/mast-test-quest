import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from server.database import SessionLocal, Base, engine
import server.crud as crud, server.schemas as schemas


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit", response_model=schemas.RecordRead)
def submit_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    """Эндпоинт для приёма новой записи. Возвращает сохранённую запись."""
    return crud.create_record(db, record)


@app.get("/records", response_model=list[schemas.RecordRead])
def get_records(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)): 
    """Эндпоинт для получения списка записей с пагинацией."""
    return crud.get_records(db, skip=skip, limit=limit)

if __name__ == "__main__":
    import uvicorn
    is_frozen = getattr(sys, 'frozen', False)  # PyInstaller ставит этот флаг
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=not is_frozen  # отключить reload в сборке
    )

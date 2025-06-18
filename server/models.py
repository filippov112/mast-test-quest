from sqlalchemy import Column, Date, Integer, String, Time
from server.database import Base


class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    click_number = Column(Integer, nullable=False)


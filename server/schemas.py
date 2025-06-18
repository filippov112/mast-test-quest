from pydantic import BaseModel
from datetime import date, time


class RecordCreate(BaseModel):
    text: str
    date: date
    time: time
    click_number: int
    
class RecordRead(BaseModel):
    id: int
    text: str
    date: date
    time: time
    click_number: int

    class ConfigDict:
        from_attributes = True


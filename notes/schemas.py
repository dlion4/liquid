from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class NoteModel(BaseModel):
    id:UUID
    title:str
    content:str
    timestamp:datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
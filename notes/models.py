from uuid import UUID
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from datetime import datetime

class Note(Base):
    __tablename__ = "notes"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(nullable=False)
    content:Mapped[str] = mapped_column(Text, nullable=False)
    timestamp:Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self):
        return f"<Note: title={self.title}>"


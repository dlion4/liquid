from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from api.settings import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    title:Mapped[str] = mapped_column(String(255))
    content:Mapped[str] = mapped_column(String(2000))


    def __repr__(self):
        return f"<Post [(title={self.title})]"



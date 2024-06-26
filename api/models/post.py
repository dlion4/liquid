from __future__ import annotations
from sqlalchemy.orm import  Mapped, mapped_column
from api.settings import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from typing import TYPE_CHECKING
from typing import List, Dict, Optional

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    title:Mapped[str] = mapped_column(String(255))
    content:Mapped[str] = mapped_column(String(2000))
    # profile_id = Column(Integer, ForeignKey('profile.id'))
    # Relationship to Profile
    # profile = relationship("Profile", back_populates="posts")

    def __repr__(self):
        return f"<Post [(title={self.title})]"
    



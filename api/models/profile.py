from api.settings import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String
from .post import Post

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    # posts = relationship("Post", back_populates="profile")



    def __repr__(self):
        return f"<Profile [(name={self.name})~ (id={self.id})]"
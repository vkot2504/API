# comments/models.py
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, text, Integer
from app.database import Base
from app.entities.users.models import User


class Comment(Base):
    __tablename__ = 'comments'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(server_default=text("Текст сообщения"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comic_id: Mapped[int] = mapped_column(ForeignKey("comics.id", ondelete="CASCADE"), nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="comments")
    comic: Mapped["Comic"] = relationship("Comic", back_populates="comments", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "user_id": self.user_id,
            "comic_id": self.comic_id
        }
        
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)

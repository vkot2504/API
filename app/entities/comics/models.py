from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey,  text, Integer
from app.database import Base, int_pk, int_null_true
from app.entities.users.models import User
from app.entities.comments.models import Comment

class Comic(Base):
    __tablename__ = 'comics'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(server_default=text("Описание комикса"))
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Рейтинг может быть NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comic_picture: Mapped[str | None]
    
    user: Mapped["User"] = relationship("User", back_populates="comics")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="comic")
   
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "rating": self.rating,
            "user_id": self.user_id,
            "comic_picture": self.comic_pucture
        }
        
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)
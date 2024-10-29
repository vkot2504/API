from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true, str_uniq_but_nullable
from passlib.context import CryptContext
from typing import List
from app.entities.roles.models import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    password: Mapped[str]
    fname: Mapped[str_null_true | None]
    lname: Mapped[str_null_true | None]
    sex: Mapped[str]
    email: Mapped[str_uniq_but_nullable | None]
    sell_history: Mapped[str_null_true | None]
    buy_history: Mapped[str_null_true | None]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1)
    profile_picture: Mapped[str | None]

    comics: Mapped[List["Comic"]] = relationship("Comic", back_populates="user", cascade="all, delete-orphan")
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")


    extend_existing = True
        
    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.fname!r}, "
                f"last_name={self.lname!r})")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "fname": self.fname,
            "lname": self.lname,
            "email": self.email,
            "sell_history": self.sell_history,
            "buy_history": self.buy_history,
            "role_id": self.role_id,
            "profile_picture": self.profile_picture
        }
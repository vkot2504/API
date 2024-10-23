import re
from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional

class Comic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: str = Field(..., description="Описание комикса")
    rating: int = Field(None, description="Рейтинг комикса")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит заказ")
    
class ComicAdd(BaseModel):
    rating: int = Field(None, description="Рейтинг комикса")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит заказ")
    description: str = Field(..., description="Описание комикса")
    
class UpdateFilter(BaseModel):
    id: int

class ComicUpdate(BaseModel):
    description: Optional[str] = Field(None, description="Описание комикса")
    rating: Optional[int] = Field(None, description="Рейтинг комикса")
    user_id: Optional[int] = Field(None, description="ID пользователя, которому принадлежит заказ")
    
class DeleteFilter(BaseModel):
    id: int

class ComicPhoto(BaseModel):
    profile_picture: Optional[str] = Field(None, description="Название изображения")
import re
from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional

class Comment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: str = Field(..., description="Описание комментария")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит комментарий")
    
class CommentAdd(BaseModel):
    user_id: int = Field(..., description="ID пользователя, которому принадлежит комментарий")
    description: str = Field(..., description="Комментарий")
    
class UpdateFilter(BaseModel):
    id: int

class CommentUpdate(BaseModel):
    description: Optional[str] = Field(None, description="Комментарий")
    user_id: Optional[int] = Field(None, description="ID пользователя, которому принадлежит заказ")
    
class DeleteFilter(BaseModel):
    id: int
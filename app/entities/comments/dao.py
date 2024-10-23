from fastapi import APIRouter
from app.service.base import BaseDAO
from app.entities.comments.models import Comment

router = APIRouter(prefix='/comments', tags=['Комментарии'])

class CommentDAO(BaseDAO):
    model = Comment
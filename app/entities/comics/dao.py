from fastapi import APIRouter
from app.service.base import BaseDAO
from app.entities.comics.models import Comic

router = APIRouter(prefix='/comics', tags=['Комиксы'])

class ComicDAO(BaseDAO):
    model = Comic
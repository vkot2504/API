from fastapi import APIRouter
from app.service.base import BaseDAO
from app.entities.orders.models import Order

router = APIRouter(prefix='/comics', tags=['Комиксы'])

class ComicDAO(BaseDAO):
    model = Comic
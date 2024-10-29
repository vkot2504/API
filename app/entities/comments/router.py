from fastapi import APIRouter, Depends, HTTPException
from app.entities.comments.dao import CommentDAO
from app.entities.comments.rb import RBComment
from app.entities.comments.schemas import Comment as SComment
from app.entities.comments.schemas import CommentAdd as SCommentAdd
from app.entities.comments.schemas import UpdateFilter, CommentUpdate, DeleteFilter

router = APIRouter(prefix='/comments', tags=['Комментарии'])


@router.get("/", summary="Показать все комментарии")
async def get_all_comments(request_body: RBComment = Depends()) -> list[SComment]:
    return await CommentDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Показать комментарий по ID")
async def get_comment_by_id(id: int) -> SComment| dict:
    result = await CommentDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Комментарий по данному ID не найден.'}
    return result

@router.post("/add", summary="Опубликовать комментарий")
async def register_user(comment: SCommentAdd) -> dict:
    check = await CommentDAO.add(**comment.dict())
    if check:
        return {"message": "Новый комментарий добавлен.", "comment": comment}
    else:
        return {"message": "Комментарий не удалось добавить."}
    
@router.put("/update/{id}", summary="Обновить комментарий по ID")
async def update_user_handler(id: int, new_data: CommentUpdate):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(description_code=400, detail="Нет данных для обновления.")
    
    check = await CommentDAO.update(id=id, update_data=update_data)
    if check:
        return {"message": "Информация о комментарии успешно обновлена."}
    else:
        raise HTTPException(description_code=400, detail="Ошибка при обновлении информации о заказе.")
    
@router.delete("/delete/{id}", summary="Удалить комментарий по ID")
async def delete_user_handler(id: int):
    check = await CommentDAO.delete(id=id)
    if check:
        return {"message": "Комментарий успешно удалён."}
    else:
        raise HTTPException(description_code=400, detail="Ошибка при удалении комментария.")
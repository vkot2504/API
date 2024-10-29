from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Request
from app.entities.comics.dao import ComicDAO
from app.entities.comics.rb import RBComic
from app.entities.users.dependencies import get_current_user, get_current_admin_user
from app.entities.comics.schemas import Comic as SComic
from app.entities.comics.schemas import ComicAdd as SComicAdd
from app.entities.comics.schemas import UpdateFilter, ComicUpdate, DeleteFilter
from fastapi.responses import FileResponse, JSONResponse
import os
from app.entities.comics.schemas import ComicPhoto
from pydantic import BaseModel

if not os.path.exists("uploads"):
    os.makedirs("uploads")

UPLOAD_FOLDER = "uploads/"
router = APIRouter(prefix='/comics', tags=['Комиксы'])


@router.get("/", summary="Показать все комиксы")
async def get_all_comics(request_body: RBComic = Depends()) -> list[SComic]:
    return await ComicDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Показать комикс по ID")
async def get_comic_by_id(id: int) -> SComic| dict:
    result = await ComicDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Комикс по данному ID не найден.'}
    return result

@router.post("/add", summary="Опубликовать комикс")
async def register_user(comic: SComicAdd) -> dict:
    check = await ComicDAO.add(**comic.dict())
    if check:
        return {"message": "Новый комикс добавлен.", "comic": comic}
    else:
        return {"message": "Комикс не удалось добавить."}
    
@router.put("/update/{id}", summary="Обновить комикс по ID")
async def update_user_handler(id: int, new_data: ComicUpdate):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(description_code=400, detail="Нет данных для обновления.")
    
    check = await ComicDAO.update(id=id, update_data=update_data)
    if check:
        return {"message": "Информация о комиксе успешно обновлена."}
    else:
        raise HTTPException(description_code=400, detail="Ошибка при обновлении информации о заказе.")
    
@router.delete("/delete/{id}", summary="Удалить комикс по ID")
async def delete_user_handler(id: int):
    check = await ComicDAO.delete(id=id)
    if check:
        return {"message": "Комикс успешно удалён."}
    else:
        raise HTTPException(description_code=400, detail="Ошибка при удалении комикса.")
@router.post("/comic_picture/{id}", summary="Загрузить изображение профиля пользователя")
async def upload_comic_picture(id: int, comic_picture: UploadFile = File(...), current_comic: ComicPhoto = Depends(get_current_user)):

    file_extension = comic_picture.filename.split(".")[-1].lower()
    if file_extension not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла. Поддерживаются только .jpg, .jpeg, .png.")
    
    file_size = await comic_picture.read()
    if len(file_size) > 5 * 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Файл слишком большой. Максимум 5MB.")

    file_location = os.path.join(UPLOAD_FOLDER, f"{id}.{file_extension}")
    
    with open(file_location, "wb") as buffer:
        buffer.write(file_size)

    update_data = {"comic_picture": file_location}
    current_user = await ComicDAO.update(id=id, update_data=update_data)
    if current_user:
        return {"message": "Изображение профиля успешно загружено."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении данных пользователя.")

@router.get("/comic_picture/{id}", summary="Получить изображение комикса")
async def get_comic_picture(id: int):
    file_path = os.path.join('uploads', f"{id}.jpg")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Изображение не найдено")

    return FileResponse(file_path)

@router.delete("/comic_picture/{id}", summary="Удалить изображение профиля пользователя")
async def delete_comic_picture(id: int, current_comic: ComicPhoto = Depends(get_current_user)):
    if current_comic.id != id and current_comic.role_id != 0:
        raise HTTPException(status_code=403, detail="Нет доступа для удаления изображения")
    
    file_path = os.path.join(UPLOAD_FOLDER, f"{id}.jpg")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    update_data = {"comic_picture": None}
    updated_comic = await ComicDAO.update(id=id, update_data=update_data)
    if updated_comic:
        return JSONResponse(content={"message": "Изображение профиля успешно удалено."})
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении изображения профиля.")
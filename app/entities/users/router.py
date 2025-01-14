from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Request
from app.entities.users.dao import UserDAO
from app.entities.users.auth import get_password_hash, authenticate_user, create_access_token
from app.entities.users.schemas import User as SUser
from app.entities.users.schemas import BaseUser, UserAuth, UserUpdate, UserPhoto
from app.entities.users.dependencies import get_current_user, get_current_admin_user
from fastapi.responses import FileResponse, JSONResponse
import os
from pydantic import BaseModel



if not os.path.exists("uploads"):
    os.makedirs("uploads")

UPLOAD_FOLDER = "uploads/"

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])

@router.get("/", summary="Получить всех пользователей")
async def get_all_users(current_admin_user: SUser = Depends(get_current_admin_user)) -> list[SUser]:
    return await UserDAO.find_all()

@router.get("/{id}", summary="Получить пользователя через ID")
async def get_user_by_id(id: int, current_user: SUser = Depends(get_current_user)) -> SUser | dict:
    result = await UserDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Пользователь по данному ID не найден.'}
    return result

@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: BaseUser) -> dict:
    user = await UserDAO.find_one_or_none(username=user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким username уже существует"
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    
    return {"message": "Вы успешно зарегистрированы!"}

@router.post("/login/", summary="Логин пользователя")
async def auth_user(response: Response, user_data: UserAuth):
    check = await authenticate_user(username=user_data.username, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль'
        )
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token)
    
    return {'access_token': access_token, 'refresh_token': None}

@router.get("/me/", summary="Получить данные текущего пользователя")
async def get_me(user_data: SUser = Depends(get_current_user)):
    return user_data

@router.post("/logout/", summary="Выйти из системы")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.put("/update/{id}", summary="Обновить пользователя по ID")
async def update_user_handler(id: int, new_data: UserUpdate, current_user: SUser = Depends(get_current_user)):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления.")
    check = await UserDAO.update(id=id, update_data=update_data)
    if check:
        return {"message": "Информация о пользователе успешно обновлена."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о пользователе.")
    
@router.delete("/delete/{id}", summary="Удалить пользователя по ID")
async def delete_user_handler(id: int, current_user: SUser = Depends(get_current_user)):
        check = await UserDAO.delete(id=id)
        if check:
            return {"message": "Пользователь успешно удалён."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при удалении пользователя.")
   
@router.post("/profile_picture/{id}", summary="Загрузить изображение профиля пользователя")
async def upload_profile_picture(id: int, profile_picture: UploadFile = File(...), current_user: UserPhoto = Depends(get_current_user)):

    file_extension = profile_picture.filename.split(".")[-1].lower()
    if file_extension not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла. Поддерживаются только .jpg, .jpeg, .png.")
    
    file_size = await profile_picture.read()
    if len(file_size) > 5 * 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Файл слишком большой. Максимум 5MB.")

    file_location = os.path.join(UPLOAD_FOLDER, f"{id}.{file_extension}")
    
    with open(file_location, "wb") as buffer:
        buffer.write(file_size)

    update_data = {"profile_picture": file_location}
    current_user = await UserDAO.update(id=id, update_data=update_data)
    if current_user:
        return {"message": "Изображение профиля успешно загружено."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении данных пользователя.")

@router.get("/profile_picture/{id}", summary="Получить изображение профиля пользователя")
async def get_profile_picture(id: int):
    file_path = os.path.join('uploads', f"{id}.jpg")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Изображение не найдено")

    return FileResponse(file_path)

@router.delete("/profile_picture/{id}", summary="Удалить изображение профиля пользователя")
async def delete_profile_picture(id: int, current_user: UserPhoto = Depends(get_current_user)):

    
    file_path = os.path.join(UPLOAD_FOLDER, f"{id}.jpg")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    update_data = {"profile_picture": None}
    updated_user = await UserDAO.update(id=id, update_data=update_data)
    if updated_user:
        return JSONResponse(content={"message": "Изображение профиля успешно удалено."})
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении изображения профиля.")
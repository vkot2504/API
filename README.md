Установка: 

1. Для начала создаем .env файл с указанием данных для входа
```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
SECRET_KEY=
ALGORITHM=
ADMIN_USERNAME=
ADMIN_PASSWORD=
```

2. Устанавливаем необходимые библиотеки: 
```
pip install -r requirements.txt
```

3. Устаналиваем FASTAPI
```
pip install fastapi uvicorn
```

4. Запускаем проект 
```
uvicorn app.main:app --reload --port 8000
```

5. В браузере запускаем 
```
localhost:8000
```
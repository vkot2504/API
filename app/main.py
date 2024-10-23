from fastapi import FastAPI
import os
from app.entities.users.router import router as router_users
from app.entities.comics.router import router as router_comics
from app.entities.roles.router import router as router_roles
from app.entities.comments.router import router as router_comments
from app.entities.roles.models import init_roles
from app.entities.users.dependencies import create_default_admin

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_roles()
    
@app.on_event("startup")
async def startup_event():
    await create_default_admin()

@app.get("/", summary="Основная страница")
def main_page():
    return {"message": "This is homepage."}

app.include_router(router_users)
app.include_router(router_comics)
app.include_router(router_roles)
app.include_router(router_comments)

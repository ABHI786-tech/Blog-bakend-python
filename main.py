from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from router.user_routers import router
from cors.database import engine, get_db
from cors.hashing import Hash
from models import usersModel
from schemas.users_schema import Create, ShowUser
from config import token
from router.blog_routes import blog_route


app = FastAPI(swagger_ui_parameters={"persistAuthorization": True})

usersModel.Base.metadata.create_all(engine)


@app.get("/")
def dashboard():
    return {"message": "Hello welcome to our Blog Dashboard"}

app.include_router(router)
app.include_router(blog_route)



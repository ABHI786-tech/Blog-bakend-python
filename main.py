from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from cors.database import engine, get_db, Base
from models import usersModel
from schemas.usersSchema import Create

app = FastAPI()

usersModel.Base.metadata.create_all(engine)

@app.get("/")
def dashboard():
    return "hello welcome to our Blog Dashboard"


@app.post("/signup")
def create(request: Create, db:Session = Depends(get_db)):
    # hashed_password = Hash.bcrypt(request.password)
    create_user =usersModel.Users(name=request.name, email=request.email, password=request.password)
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user
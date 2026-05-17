from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import token
from models.usersModel import Users
from cors.database import get_db
from cors.hashing import Hash
from schemas.users_schema import Create, ShowUser

router = APIRouter()


@router.post("/signup")
def create(request: Create, db: Session = Depends(get_db)):

    hashed_password = Hash.bcrypt(request.password)

    create_user = Users(
        name=request.name, email=request.email, password=hashed_password
    )

    db.add(create_user)
    db.commit()
    db.refresh(create_user)

    return "user Register Successfully"


@router.get("/profile", response_model=List[ShowUser])
def get_users(
    current_user: Users = Depends(token.get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(Users).all()
    return users


@router.post('/login')
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(Users).filter(
        Users.email == request.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = token.create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

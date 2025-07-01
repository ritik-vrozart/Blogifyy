from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user import User
from app.schemas.users import RegisterUser

auth_api = APIRouter()

@auth_api.get("/auth")
def auth():
    return {"message": "Hello, World!"}

@auth_api.post("/register")
def register(request: RegisterUser,db: Session = Depends(get_db)):
    print(request)
    new_user = db.add(User(username=request.username, email=request.email, password=request.password))
    db.commit()
    # db.refresh(new_user)
    return {"message": "User registered successfully"}
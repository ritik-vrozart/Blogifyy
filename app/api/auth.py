from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.db import get_db
from app.models.user import User
from app.schemas.users import LoginUser, RegisterUser
from app.utils.auth_utils import create_access_token, verify_token

auth_api = APIRouter()

@auth_api.get("/auth")
def auth():
    return {"message": "Hello, World!"}

@auth_api.post("/register")
def register(request: RegisterUser,db: Session = Depends(get_db)):
    print(request)
    new_user = User(username=request.username, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    # db.refresh(new_user)
    return {"message": "User registered successfully"}


@auth_api.post("/login")
def login(request: LoginUser,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    return {"message": "User logged in successfully","data":{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "access_token": access_token
    }}


@auth_api.get("/me")
def me(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")




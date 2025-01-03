from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.dependencies import get_db
from app.security import get_password_hash, SECRET_KEY
import jwt

router = APIRouter()

@router.get("/admin/users")
def list_users(token: str, db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("role") not in ["admin", "root"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return db.query(User).all()

@router.post("/admin/users", response_model=UserResponse)
def create_user(token: str, user: UserCreate, db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if payload.get("role") != "root":
        raise HTTPException(status_code=403, detail="Only root can create users")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role,
        client=user.client,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User, Role, UserRole
from app.security import create_access_token
import logging

router = APIRouter()

@router.post("/token")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Log database connection details
    engine = db.get_bind()
    database_url = str(engine.url)
    logging.debug(f"Connected to database: {database_url}, username: {username}")

    # Fetch user details by login ID
    user = db.query(User).filter(User.user_login_id == username, User.active_flag == 1).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    # Verify plain text password
    if password != user.user_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    # Fetch roles for the user
    user_roles = (
        db.query(Role.role_name)
        .join(UserRole, Role.id == UserRole.role_id)
        .filter(UserRole.user_id == user.id, UserRole.active_flag == 1, Role.active_flag == 1)
        .all()
    )
    
    roles = [role.role_name for role in user_roles]

    if not roles:
        raise HTTPException(
            status_code=403,
            detail="User has no assigned roles or roles are inactive.",
        )

    # Debug logging for roles and user details
    logging.debug(f"User: {user.user_first_name} {user.user_last_name}, Roles: {roles}, Client ID: {user.client_id}")

    # Generate access token
    access_token = create_access_token(data={"sub": user.user_login_id, "roles": roles})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "roles": roles[0],
        "client_id": user.client_id,
        "user_full_name": f"{user.user_first_name} {user.user_last_name}",
    }

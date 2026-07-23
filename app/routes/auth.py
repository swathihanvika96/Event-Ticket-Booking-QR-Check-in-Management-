from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_admin
)

from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# -------------------------
# Register User
# -------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return AuthService.register(
        db,
        user
    )


# -------------------------
# Login User
# -------------------------
@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    return AuthService.login(
        db,
        form_data.username,
        form_data.password
    )


# -------------------------
# Current User
# -------------------------
@router.get(
    "/me",
    response_model=UserResponse
)
def profile(
    current_user=Depends(get_current_user)
):

    return current_user



# -------------------------
# Admin - Get Users
# -------------------------
@router.get(
    "/users"
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    return AuthService.get_all_users(db)



# -------------------------
# Admin - Get User By ID
# -------------------------
@router.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id:int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    return AuthService.get_user(
        db,
        user_id
    )



# -------------------------
# Admin - Delete User
# -------------------------
@router.delete(
    "/users/{user_id}"
)
def delete_user(
    user_id:int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    return AuthService.delete_user(
        db,
        user_id
    )



# -------------------------
# Activate User
# -------------------------
@router.put(
    "/users/{user_id}/activate"
)
def activate_user(
    user_id:int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    return AuthService.activate_user(
        db,
        user_id
    )



# -------------------------
# Deactivate User
# -------------------------
@router.put(
    "/users/{user_id}/deactivate"
)
def deactivate_user(
    user_id:int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    return AuthService.deactivate_user(
        db,
        user_id
    )
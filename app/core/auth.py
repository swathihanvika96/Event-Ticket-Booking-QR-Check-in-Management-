from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return AuthService.register(db, user)

    except Exception as e:
        print("REGISTER ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
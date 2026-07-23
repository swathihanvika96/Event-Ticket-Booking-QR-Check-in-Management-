from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:


    # ==========================
    # Register User
    # ==========================
    @staticmethod
    def register(
        db: Session,
        user: UserCreate
    ):

        try:

            # Check existing email
            existing_user = (
                db.query(User)
                .filter(User.email == user.email)
                .first()
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )


            new_user = User(
                name=user.name,
                email=user.email,
                hashed_password=hash_password(
                    user.password
                ),
                role=user.role,
                is_active=True
            )


            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user


        except HTTPException:
            raise


        except Exception as e:

            db.rollback()

            print("REGISTER ERROR:", e)

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )



    # ==========================
    # Login User
    # ==========================
    @staticmethod
    def login(
        db: Session,
        username: str,
        password: str
    ):

        user = (
            db.query(User)
            .filter(User.email == username)
            .first()
        )


        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )


        if not verify_password(
            password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )


        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="User account is inactive"
            )


        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role
            }
        )


        return {
            "access_token": token,
            "token_type": "bearer"
        }



    # ==========================
    # Get All Users
    # ==========================
    @staticmethod
    def get_all_users(
        db: Session
    ):

        return db.query(User).all()



    # ==========================
    # Get User By ID
    # ==========================
    @staticmethod
    def get_user(
        db: Session,
        user_id: int
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )


        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )


        return user



    # ==========================
    # Delete User
    # ==========================
    @staticmethod
    def delete_user(
        db: Session,
        user_id: int
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )


        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )


        db.delete(user)
        db.commit()


        return {
            "message": "User deleted successfully"
        }



    # ==========================
    # Activate User
    # ==========================
    @staticmethod
    def activate_user(
        db: Session,
        user_id: int
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )


        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )


        user.is_active = True

        db.commit()
        db.refresh(user)


        return {
            "message": "User activated successfully"
        }



    # ==========================
    # Deactivate User
    # ==========================
    @staticmethod
    def deactivate_user(
        db: Session,
        user_id: int
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )


        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )


        user.is_active = False

        db.commit()
        db.refresh(user)


        return {
            "message": "User deactivated successfully"
        }
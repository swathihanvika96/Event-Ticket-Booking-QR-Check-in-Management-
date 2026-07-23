from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    user_id = payload.get("sub")

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user



# ADMIN access
def require_admin(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user



# ORGANIZER access
def require_organizer(
    current_user: User = Depends(get_current_user)
):

    if current_user.role not in [
        "ADMIN",
        "ORGANIZER"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Organizer access required"
        )

    return current_user



# ATTENDEE access
def require_attendee(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "ATTENDEE":

        raise HTTPException(
            status_code=403,
            detail="Attendee access required"
        )

    return current_user
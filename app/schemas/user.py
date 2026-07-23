from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    name: str
    email: EmailStr
    password: str
    role: str = "ATTENDEE"



class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True



class Token(BaseModel):

    access_token: str
    token_type: str
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="Password@123")
    role: str = Field(..., example="Organizer")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="Password@123")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
from pydantic import BaseModel
from typing import Optional


class CheckInResponse(BaseModel):
    message: str
    booking_id: int
    event_id: int
    attendee_id: int
    checked_in: bool

    class Config:
        from_attributes = True



class AttendeeResponse(BaseModel):
    attendee_id: int
    username: str
    email: str
    booking_id: int
    checked_in: bool

    class Config:
        from_attributes = True
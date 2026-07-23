from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class BookingCreate(BaseModel):
    event_id: int

    ticket_count: int = Field(..., gt=0)


class BookingUpdate(BaseModel):
    booking_status: str


class BookingResponse(BaseModel):
    id: int
    booking_number: str
    attendee_id: int
    event_id: int
    ticket_count: int
    total_amount: float
    booking_status: str
    qr_code: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class EventCreate(BaseModel):
    event_name: str = Field(..., example="Python Conference")

    venue: str = Field(..., example="Hyderabad")

    event_date: datetime

    total_tickets: int = Field(..., gt=0)

    ticket_price: float = Field(..., gt=0)

    status: str = Field(default="Upcoming")

    @field_validator("event_date")
    @classmethod
    def validate_future_date(cls, value):
        if value <= datetime.now():
            raise ValueError(
                "Event date must be a future date."
            )
        return value


class EventUpdate(BaseModel):
    event_name: str | None = None
    venue: str | None = None
    event_date: datetime | None = None
    total_tickets: int | None = Field(default=None, gt=0)
    ticket_price: float | None = Field(default=None, gt=0)
    status: str | None = None


class EventResponse(BaseModel):
    id: int
    event_name: str
    venue: str
    event_date: datetime
    total_tickets: int
    available_tickets: int
    ticket_price: float
    status: str
    organizer_id: int

    model_config = ConfigDict(from_attributes=True)
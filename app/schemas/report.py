from pydantic import BaseModel
from typing import List


class EventReportResponse(BaseModel):
    event_id: int
    event_name: str
    total_tickets: int
    sold_tickets: int
    available_tickets: int

    class Config:
        from_attributes = True



class BookingHistoryResponse(BaseModel):
    booking_id: int
    event_id: int
    attendee_id: int
    ticket_count: int
    total_amount: float
    booking_status: str

    class Config:
        from_attributes = True



class AttendeeReportResponse(BaseModel):
    attendee_id: int
    username: str
    email: str
    total_bookings: int

    class Config:
        from_attributes = True



class SalesReportResponse(BaseModel):
    total_bookings: int
    total_tickets_sold: int
    total_revenue: float

    class Config:
        from_attributes = True



class PaginatedReportResponse(BaseModel):
    page: int
    limit: int
    total: int
    data: List[EventReportResponse]

    class Config:
        from_attributes = True
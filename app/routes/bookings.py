from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
)

from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse,
)

from app.services.booking_service import BookingService


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Ticket Booking",
    description="""
Book tickets for an event.

Rules:
- Only attendees can book tickets.
- Ticket availability will reduce automatically.
- Booking cannot exceed available tickets.
"""
)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BookingService.create_booking(
        db,
        booking,
        current_user
    )


@router.get(
    "/",
    response_model=list[BookingResponse],
    summary="Get Bookings",
    description="""
Get booking list.

Rules:
- Admin can view all bookings.
- Organizer can view bookings for their events.
- Attendee can view only their own bookings.
"""
)
def get_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BookingService.get_bookings(
        db,
        current_user
    )


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
    summary="Get Booking By ID"
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BookingService.get_booking(
        db,
        booking_id,
        current_user
    )


@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
    summary="Update Booking Status",
    description="""
Update booking status.

Available statuses:
- Booked
- Confirmed
- Cancelled

When cancelled:
- Ticket availability will be restored.
"""
)
def update_booking(
    booking_id: int,
    booking: BookingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BookingService.update_booking(
        db,
        booking_id,
        booking,
        current_user
    )
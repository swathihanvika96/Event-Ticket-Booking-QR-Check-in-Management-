from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.schemas.checkin import CheckInResponse, AttendeeResponse

from app.services.checkin_service import CheckInService


router = APIRouter(
    prefix="/checkin",
    tags=["QR Check-in"]
)


@router.post(
    "/{booking_id}",
    response_model=CheckInResponse,
    status_code=status.HTTP_200_OK,
    summary="Check-in Ticket",
    description="""
Verify attendee ticket and perform QR check-in.

Rules:
- Booking must exist.
- Booking status must be Confirmed.
- QR check-in is allowed only once.
- Cancelled bookings cannot check in.
"""
)
def check_in(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CheckInService.check_in(
        db,
        booking_id,
        current_user
    )


@router.get(
    "/events/{event_id}/attendees",
    response_model=list[AttendeeResponse],
    summary="Get Event Attendees",
    description="""
Get all attendees for an event.

Permissions:
- Admin can view all attendees.
- Organizer can view attendees of their events.
"""
)
def get_event_attendees(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CheckInService.get_event_attendees(
        db,
        event_id,
        current_user
    )
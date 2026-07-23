from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.schemas.report import (
    BookingHistoryResponse,
    EventReportResponse,
)

from app.services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get(
    "/booking-history/{attendee_id}",
    response_model=list[BookingHistoryResponse],
    summary="Attendee Booking History",
    description="""
Get booking history of an attendee.

Rules:
- Attendee can view only their own history.
- Admin can view any attendee history.
"""
)
def booking_history(
    attendee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ReportService.get_booking_history(
        db,
        attendee_id,
        current_user
    )


@router.get(
    "/events/{event_id}/ticket-summary",
    response_model=EventReportResponse,
    summary="Event Ticket Report",
    description="""
View ticket sales summary.

Returns:
- Total tickets
- Sold tickets
- Available tickets
- Revenue generated
"""
)
def event_ticket_report(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ReportService.get_event_ticket_report(
        db,
        event_id,
        current_user
    )


@router.get(
    "/dashboard",
    summary="Dashboard Report",
    description="""
Admin dashboard report.

Includes:
- Total events
- Total bookings
- Total revenue
- Ticket statistics
"""
)
def dashboard_report(
    page: int = Query(
        1,
        ge=1,
        description="Page number"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Records per page"
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ReportService.dashboard(
        db,
        current_user,
        page,
        limit
    )
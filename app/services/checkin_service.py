from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.event import Event
from app.models.user import User

from app.schemas.checkin import CheckInResponse, AttendeeResponse

class CheckInService:

    @staticmethod
    def check_in(
        db: Session,
        booking_id: int,
        current_user: User
    ):

        booking = (
            db.query(Booking)
            .filter(
                Booking.id == booking_id
            )
            .first()
        )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )


        # Attendee can check only own ticket
        if (
            current_user.role.lower() == "attendee"
            and booking.attendee_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can check-in only your own booking"
            )


        if booking.booking_status == "Cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancelled booking cannot be checked-in"
            )


        # Already checked in
        if booking.is_checked_in:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket already checked-in"
            )


        booking.is_checked_in = True


        db.commit()
        db.refresh(booking)


        return {
            "message": "Check-in successful",
            "booking_id": booking.id,
            "event_id": booking.event_id,
            "attendee_id": booking.attendee_id,
            "checked_in": True
        }



    @staticmethod
    def get_event_attendees(
        db: Session,
        event_id: int,
        current_user: User
    ):

        event = (
            db.query(Event)
            .filter(
                Event.id == event_id
            )
            .first()
        )


        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )


        # Organizer can view only own events
        if (
            current_user.role.lower() == "organizer"
            and event.organizer_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot view this event attendees"
            )


        bookings = (
            db.query(Booking)
            .filter(
                Booking.event_id == event_id,
                Booking.booking_status != "Cancelled"
            )
            .all()
        )


        attendees = []


        for booking in bookings:

            user = (
                db.query(User)
                .filter(
                    User.id == booking.attendee_id
                )
                .first()
            )


            if user:
                attendees.append(
                    {
                        "attendee_id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "booking_id": booking.id,
                        "checked_in": booking.is_checked_in
                    }
                )


        return attendees
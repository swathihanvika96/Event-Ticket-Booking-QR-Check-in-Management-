import os
import uuid

import qrcode
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.event import Event
from app.models.user import User
from app.schemas.booking import BookingCreate
from app.utils.enums import (
    BookingStatus,
    EventStatus,
    UserRole
)


class BookingService:

    QR_FOLDER = "qr_codes"

    @staticmethod
    def generate_booking_number():

        return f"BK-{uuid.uuid4().hex[:10].upper()}"

    @staticmethod
    def generate_qr_code(booking_number: str):

        os.makedirs(
            BookingService.QR_FOLDER,
            exist_ok=True
        )

        file_name = f"{booking_number}.png"

        file_path = os.path.join(
            BookingService.QR_FOLDER,
            file_name
        )

        qr = qrcode.make(booking_number)

        qr.save(file_path)

        return file_path

    @staticmethod
    def create_booking(
        db: Session,
        booking: BookingCreate,
        current_user: User
    ):

        # Only attendees can book tickets
        if current_user.role != UserRole.ATTENDEE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only attendees can book tickets."
            )

        event = (
            db.query(Event)
            .filter(Event.id == booking.event_id)
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found."
            )

        if event.status == EventStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event has been cancelled."
            )

        if event.status == EventStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event already completed."
            )

        if booking.ticket_count > event.available_tickets:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough tickets available."
            )

        booking_number = (
            BookingService.generate_booking_number()
        )

        qr_path = (
            BookingService.generate_qr_code(
                booking_number
            )
        )

        total_amount = (
            booking.ticket_count
            * float(event.ticket_price)
        )

        new_booking = Booking(
            booking_number=booking_number,
            attendee_id=current_user.id,
            event_id=booking.event_id,
            ticket_count=booking.ticket_count,
            total_amount=total_amount,
            booking_status=BookingStatus.BOOKED,
            qr_code=qr_path
        )

        # Reduce available tickets
        event.available_tickets -= booking.ticket_count

        db.add(new_booking)

        db.commit()

        db.refresh(new_booking)

        return {
            "message": "Booking created successfully.",
            "data": new_booking
        }

    @staticmethod
    def get_bookings(
        db: Session,
        current_user: User,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Booking)

        # Admin can view all bookings
        if current_user.role == UserRole.ADMIN:
            pass

        # Organizer can view bookings for their events
        elif current_user.role == UserRole.ORGANIZER:

            query = (
                query.join(Event)
                .filter(Event.organizer_id == current_user.id)
            )

        # Attendee can view only their bookings
        elif current_user.role == UserRole.ATTENDEE:

            query = query.filter(
                Booking.attendee_id == current_user.id
            )

        total_records = query.count()

        bookings = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "data": bookings
        }

    @staticmethod
    def get_booking_by_id(
        db: Session,
        booking_id: int,
        current_user: User
    ):

        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found."
            )

        # Admin can access any booking
        if current_user.role == UserRole.ADMIN:
            return booking

        # Organizer can access bookings only for their events
        if current_user.role == UserRole.ORGANIZER:

            event = (
                db.query(Event)
                .filter(Event.id == booking.event_id)
                .first()
            )

            if not event or event.organizer_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied."
                )

            return booking

        # Attendee can access only their own booking
        if booking.attendee_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        return booking

    @staticmethod
    def get_booking_history(
        db: Session,
        attendee_id: int,
        current_user: User,
        page: int = 1,
        limit: int = 10
    ):

        # Attendees can only view their own history
        if (
            current_user.role == UserRole.ATTENDEE
            and current_user.id != attendee_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own booking history."
            )

        query = db.query(Booking)

        # Organizer can view attendee history only for bookings
        # related to their own events
        if current_user.role == UserRole.ORGANIZER:

            query = (
                query.join(Event)
                .filter(
                    Event.organizer_id == current_user.id,
                    Booking.attendee_id == attendee_id
                )
            )

        else:
            query = query.filter(
                Booking.attendee_id == attendee_id
            )

        total_records = query.count()

        bookings = (
            query
            .order_by(Booking.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "data": bookings
        }

    @staticmethod
    def update_booking(
        db: Session,
        booking_id: int,
        booking_data,
        current_user: User
    ):

        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found."
            )

        event = (
            db.query(Event)
            .filter(Event.id == booking.event_id)
            .first()
        )

        # Permission Check
        if current_user.role == UserRole.ATTENDEE:

            if booking.attendee_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied."
                )

        elif current_user.role == UserRole.ORGANIZER:

            if event.organizer_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied."
                )

        # Already Cancelled
        if (
            booking.booking_status ==
            BookingStatus.CANCELLED
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking already cancelled."
            )

        # Cancel Booking
        if (
            booking_data.booking_status ==
            BookingStatus.CANCELLED
        ):

            booking.booking_status = BookingStatus.CANCELLED

            # Restore tickets
            event.available_tickets += booking.ticket_count

        elif (
            booking_data.booking_status ==
            BookingStatus.CONFIRMED
        ):

            booking.booking_status = BookingStatus.CONFIRMED

        elif (
            booking_data.booking_status ==
            BookingStatus.BOOKED
        ):

            booking.booking_status = BookingStatus.BOOKED

        db.commit()
        db.refresh(booking)

        return {
            "message": "Booking updated successfully.",
            "data": booking
        }

    @staticmethod
    def confirm_booking(
        db: Session,
        booking_id: int
    ):

        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found."
            )

        if booking.booking_status == BookingStatus.CANCELLED:
            raise HTTPException(
                status_code=400,
                detail="Cancelled booking cannot be confirmed."
            )

        booking.booking_status = BookingStatus.CONFIRMED

        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def get_ticket_count(
        db: Session,
        event_id: int
    ):

        event = (
            db.query(Event)
            .filter(Event.id == event_id)
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found."
            )

        sold = (
            event.total_tickets
            - event.available_tickets
        )

        return {
            "event_id": event.id,
            "event_name": event.event_name,
            "total_tickets": event.total_tickets,
            "sold_tickets": sold,
            "available_tickets": event.available_tickets
        }
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from datetime import datetime

from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate
from app.utils.enums import EventStatus, UserRole


class EventService:

    @staticmethod
    def create_event(
        db: Session,
        event: EventCreate,
        current_user: User
    ):

        # Only Admin and Organizer can create events
        if current_user.role not in [
            UserRole.ADMIN,
            UserRole.ORGANIZER
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Admin or Organizer can create events."
            )

        new_event = Event(
            event_name=event.event_name,
            venue=event.venue,
            event_date=event.event_date,
            total_tickets=event.total_tickets,
            available_tickets=event.total_tickets,
            ticket_price=event.ticket_price,
            status=event.status,
            organizer_id=current_user.id
        )

        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        return {
            "message": "Event created successfully.",
            "data": new_event
        }

    @staticmethod
    def get_events(
        db: Session,
        page: int = 1,
        limit: int = 10,
        name: str | None = None,
        venue: str | None = None,
        status_filter: str | None = None
    ):

        query = db.query(Event)

        # Search by event name
        if name:
            query = query.filter(
                Event.event_name.ilike(f"%{name}%")
            )

        # Search by venue
        if venue:
            query = query.filter(
                Event.venue.ilike(f"%{venue}%")
            )

        # Filter by status
        if status_filter:
            query = query.filter(
                Event.status == status_filter
            )

        total_records = query.count()

        events = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "data": events
        }


    @staticmethod
    def get_event_by_id(
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found."
            )

        return event

    @staticmethod
    def update_event(
        db: Session,
        event_id: int,
        event_data,
        current_user: User
    ):

        event = (
            db.query(Event)
            .filter(Event.id == event_id)
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found."
            )

        # Permission Check
        if current_user.role != UserRole.ADMIN:

            if current_user.role != UserRole.ORGANIZER:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied."
                )

            if event.organizer_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can update only your own events."
                )

        # Event Name
        if event_data.event_name is not None:
            event.event_name = event_data.event_name

        # Venue
        if event_data.venue is not None:
            event.venue = event_data.venue

        # Event Date
        if event_data.event_date is not None:

            if event_data.event_date <= datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Event date must be in the future."
                )

            event.event_date = event_data.event_date

        # Total Tickets
        if event_data.total_tickets is not None:

            booked = (
                event.total_tickets
                - event.available_tickets
            )

            if event_data.total_tickets < booked:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Total tickets cannot be less than booked tickets."
                )

            difference = (
                event_data.total_tickets
                - event.total_tickets
            )

            event.total_tickets = event_data.total_tickets

            event.available_tickets += difference

        # Ticket Price
        if event_data.ticket_price is not None:

            if event_data.ticket_price <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ticket price must be greater than zero."
                )

            event.ticket_price = event_data.ticket_price

        # Status
        if event_data.status is not None:

            event.status = event_data.status

        db.commit()

        db.refresh(event)

        return {
            "message": "Event updated successfully.",
            "data": event
        }
    @staticmethod
    def delete_event(
        db: Session,
        event_id: int,
        current_user: User
    ):

        event = (
            db.query(Event)
            .filter(Event.id == event_id)
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found."
            )

        # Permission Check
        if current_user.role != UserRole.ADMIN:

            if current_user.role != UserRole.ORGANIZER:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied."
                )

            if event.organizer_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can delete only your own events."
                )

        db.delete(event)
        db.commit()

        return {
            "message": "Event deleted successfully."
        }

    @staticmethod
    def get_events_by_organizer(
        db: Session,
        organizer_id: int,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Event)
            .filter(Event.organizer_id == organizer_id)
        )

        total_records = query.count()

        events = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "data": events
        }

    @staticmethod
    def get_ticket_summary(
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found."
            )

        sold = event.total_tickets - event.available_tickets

        return {
            "event_id": event.id,
            "event_name": event.event_name,
            "total_tickets": event.total_tickets,
            "sold_tickets": sold,
            "available_tickets": event.available_tickets
        }

    @staticmethod
    def update_event_status(
        db: Session,
        event_id: int,
        status_value: str,
        current_user: User
    ):

        event = (
            db.query(Event)
            .filter(Event.id == event_id)
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found."
            )

        if current_user.role != UserRole.ADMIN:

            if event.organizer_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied."
                )

        event.status = status_value

        db.commit()
        db.refresh(event)

        return {
            "message": "Event status updated successfully.",
            "data": event
        }
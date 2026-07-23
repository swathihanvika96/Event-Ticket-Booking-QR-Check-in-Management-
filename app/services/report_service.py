from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.event import Event
from app.models.booking import Booking
from app.models.checkin import CheckIn


class ReportService:

    @staticmethod
    def dashboard(db: Session):
        """Overall dashboard statistics"""

        total_users = db.query(User).count()
        total_events = db.query(Event).count()
        total_bookings = db.query(Booking).count()
        total_checkins = db.query(CheckIn).count()

        total_revenue = (
            db.query(func.sum(Booking.total_amount))
            .filter(Booking.status == "Confirmed")
            .scalar()
        ) or 0

        return {
            "total_users": total_users,
            "total_events": total_events,
            "total_bookings": total_bookings,
            "total_checkins": total_checkins,
            "total_revenue": float(total_revenue)
        }

    @staticmethod
    def booking_report(db: Session):
        """List all bookings"""

        bookings = db.query(Booking).all()

        report = []

        for booking in bookings:
            event = db.query(Event).filter(
                Event.id == booking.event_id
            ).first()

            user = db.query(User).filter(
                User.id == booking.user_id
            ).first()

            report.append({
                "booking_id": booking.id,
                "user": user.username if user else "",
                "event": event.title if event else "",
                "seat_number": booking.seat_number,
                "ticket_count": booking.ticket_count,
                "amount": booking.total_amount,
                "status": booking.status,
                "booking_date": booking.created_at
            })

        return report

    @staticmethod
    def event_report(db: Session):
        """Event-wise booking report"""

        events = db.query(Event).all()

        data = []

        for event in events:

            booking_count = db.query(Booking).filter(
                Booking.event_id == event.id
            ).count()

            checked_in = db.query(CheckIn).filter(
                CheckIn.event_id == event.id
            ).count()

            revenue = (
                db.query(func.sum(Booking.total_amount))
                .filter(
                    Booking.event_id == event.id,
                    Booking.status == "Confirmed"
                )
                .scalar()
            ) or 0

            data.append({
                "event_id": event.id,
                "title": event.title,
                "venue": event.venue,
                "capacity": event.capacity,
                "tickets_booked": booking_count,
                "checked_in": checked_in,
                "revenue": float(revenue)
            })

        return data

    @staticmethod
    def revenue_report(db: Session):
        """Revenue grouped by event"""

        revenue = (
            db.query(
                Event.title,
                func.sum(Booking.total_amount)
            )
            .join(Booking, Booking.event_id == Event.id)
            .filter(Booking.status == "Confirmed")
            .group_by(Event.title)
            .all()
        )

        result = []

        for event_name, amount in revenue:
            result.append({
                "event": event_name,
                "revenue": float(amount)
            })

        return result

    @staticmethod
    def attendance_report(db: Session):
        """Attendance percentage for each event"""

        events = db.query(Event).all()

        report = []

        for event in events:

            booked = db.query(Booking).filter(
                Booking.event_id == event.id
            ).count()

            checked = db.query(CheckIn).filter(
                CheckIn.event_id == event.id
            ).count()

            percentage = 0

            if booked > 0:
                percentage = round((checked / booked) * 100, 2)

            report.append({
                "event": event.title,
                "tickets_booked": booked,
                "checked_in": checked,
                "attendance_percentage": percentage
            })

        return report

    @staticmethod
    def checkin_report(db: Session):
        """Detailed check-in report"""

        checkins = db.query(CheckIn).all()

        report = []

        for checkin in checkins:

            booking = db.query(Booking).filter(
                Booking.id == checkin.booking_id
            ).first()

            user = db.query(User).filter(
                User.id == checkin.user_id
            ).first()

            event = db.query(Event).filter(
                Event.id == checkin.event_id
            ).first()

            report.append({
                "checkin_id": checkin.id,
                "user": user.username if user else "",
                "event": event.title if event else "",
                "seat_number": booking.seat_number if booking else "",
                "checked_in_at": checkin.checked_in_at
            })

        return report

    @staticmethod
    def user_booking_report(db: Session, user_id: int):
        """Bookings for a specific user"""

        bookings = db.query(Booking).filter(
            Booking.user_id == user_id
        ).all()

        data = []

        for booking in bookings:

            event = db.query(Event).filter(
                Event.id == booking.event_id
            ).first()

            data.append({
                "booking_id": booking.id,
                "event": event.title if event else "",
                "ticket_count": booking.ticket_count,
                "seat_number": booking.seat_number,
                "amount": booking.total_amount,
                "status": booking.status,
                "booking_date": booking.created_at
            })

        return data
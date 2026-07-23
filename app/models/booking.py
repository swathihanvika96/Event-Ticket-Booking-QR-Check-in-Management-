from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Enum,
    Numeric,
    String,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.utils.enums import BookingStatus


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    booking_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    attendee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    ticket_count = Column(
        Integer,
        nullable=False
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    booking_status = Column(
        Enum(BookingStatus),
        default=BookingStatus.BOOKED,
        nullable=False
    )

    qr_code = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    attendee = relationship(
        "User",
        back_populates="bookings"
    )

    event = relationship(
        "Event",
        back_populates="bookings"
    )

    checkin = relationship(
        "CheckIn",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan"
    )
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.utils.enums import EventStatus


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    event_name = Column(String(150), nullable=False)

    venue = Column(String(200), nullable=False)

    event_date = Column(DateTime, nullable=False)

    total_tickets = Column(Integer, nullable=False)

    available_tickets = Column(Integer, nullable=False)

    ticket_price = Column(Numeric(10, 2), nullable=False)

    status = Column(
        Enum(EventStatus),
        default=EventStatus.UPCOMING,
        nullable=False
    )

    organizer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    organizer = relationship(
        "User",
        back_populates="events"
    )

    bookings = relationship(
        "Booking",
        back_populates="event",
        cascade="all, delete-orphan"
    )
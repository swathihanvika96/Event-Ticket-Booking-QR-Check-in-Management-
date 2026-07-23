from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum,
    DateTime
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String(100),
        nullable=False
    )


    email = Column(
        String(100),
        unique=True,
        nullable=False
    )


    hashed_password = Column(
        String(255),
        nullable=False
    )


    role = Column(
        Enum(
            "ADMIN",
            "ORGANIZER",
            "ATTENDEE"
        ),
        nullable=False
    )


    is_active = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    # Organizer -> Events
    events = relationship(
        "Event",
        back_populates="organizer",
        cascade="all, delete-orphan"
    )


    # Attendee -> Bookings
    bookings = relationship(
        "Booking",
        back_populates="attendee",
        cascade="all, delete-orphan"
    )
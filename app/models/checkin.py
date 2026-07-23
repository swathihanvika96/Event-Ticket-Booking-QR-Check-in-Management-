from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class CheckIn(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        unique=True,
        nullable=False
    )

    checked_in = Column(
        Boolean,
        default=False
    )

    checked_in_time = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    booking = relationship(
        "Booking",
        back_populates="checkin"
    )
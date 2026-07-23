from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    ORGANIZER = "Organizer"
    ATTENDEE = "Attendee"


class EventStatus(str, Enum):
    UPCOMING = "Upcoming"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class BookingStatus(str, Enum):
    BOOKED = "Booked"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
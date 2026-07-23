# routes/__init__.py

from .auth import router as auth_router
from .events import router as events_router
from .bookings import router as bookings_router
from .checkin import router as checkin_router
from .reports import router as reports_router

__all__ = [
    "auth_router",
    "events_router",
    "bookings_router",
    "checkin_router",
    "reports_router",
]
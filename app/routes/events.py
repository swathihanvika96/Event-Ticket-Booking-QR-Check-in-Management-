from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_admin,
    require_organizer,
)

from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventResponse,
)

from app.services.event_service import EventService


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Event",
    description="""
Create a new event.

Permissions:
- Admin can create any event.
- Organizer can create events.
- Attendee cannot create events.
"""
)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_organizer)
):
    return EventService.create_event(
        db,
        event,
        current_user
    )


@router.get(
    "/",
    response_model=list[EventResponse],
    summary="Get Events",
    description="""
Get all events with search, filtering and pagination.

Filters:
- Search by event name
- Search by venue
- Filter by status
- Pagination using page and limit
"""
)
def get_events(
    name: Optional[str] = Query(
        None,
        description="Search event by name"
    ),
    venue: Optional[str] = Query(
        None,
        description="Search event by venue"
    ),
    status: Optional[str] = Query(
        None,
        description="Filter by event status"
    ),
    page: int = Query(
        1,
        ge=1,
        description="Page number"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Records per page"
    ),
    db: Session = Depends(get_db)
):
    return EventService.get_events(
        db,
        name=name,
        venue=venue,
        status=status,
        page=page,
        limit=limit
    )


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get Event By ID"
)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    return EventService.get_event(
        db,
        event_id
    )


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update Event",
    description="""
Update event details.

Permissions:
- Admin can update any event.
- Organizer can update only their own events.
"""
)
def update_event(
    event_id: int,
    event: EventUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_organizer)
):
    return EventService.update_event(
        db,
        event_id,
        event,
        current_user
    )


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Event",
    description="""
Delete an event.

Permissions:
- Admin can delete any event.
- Organizer can delete only their own events.
"""
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_organizer)
):
    return EventService.delete_event(
        db,
        event_id,
        current_user
    )
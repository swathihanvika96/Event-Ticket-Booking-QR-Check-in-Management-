from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine

from app.routes.auth import router as auth_router
from app.routes.events import router as events_router
from app.routes.bookings import router as bookings_router
from app.routes.checkin import router as checkin_router
from app.routes.reports import router as reports_router


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Ticket Booking & QR Check-in Management System",
    description="""
## Event Ticket Booking & QR Check-in Management API

This API provides:

- JWT Authentication
- Role-Based Authorization (Admin/User)
- Event Management
- Ticket Booking
- QR Code Generation & Verification
- Event Check-in
- Dashboard & Reports
- Swagger UI Authentication

### Roles

#### Admin
- Manage Users
- Manage Events
- View All Bookings
- Verify QR Codes
- Perform Check-in
- View Reports

#### User
- Register
- Login
- View Events
- Book Tickets
- Cancel Booking
- View Booking History
- Download QR Code
""",
    version="1.0.0",
    contact={
        "name": "Stackly Python Developer",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    }
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(bookings_router)
app.include_router(checkin_router)
app.include_router(reports_router)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Event Ticket Booking & QR Check-in Management System",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "Healthy",
        "application": "Event Ticket Booking API"
    }
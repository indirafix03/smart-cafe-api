from fastapi import FastAPI
from database import engine, Base
from routers import auth_router, table_router, reservation_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Cafe API",
    description="Reservation system for Smart Cafe",
    version="1.0.0"
)

# Include routers
app.include_router(auth_router.router)
app.include_router(table_router.router)
app.include_router(reservation_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to Smart Cafe API", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.reservation import Reservation
from models.table import Table
from schemas.reservation_schema import ReservationCreate, ReservationResponse
from auth.dependencies import get_current_user
from models.user import User
from datetime import datetime

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReservationResponse)
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if table exists
    table = db.query(Table).filter(Table.id == reservation.table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    
    # 🔴 DOUBLE BOOKING VALIDATION (KRITIS)
    conflict = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id,
        Reservation.start_time < reservation.end_time,
        Reservation.end_time > reservation.start_time
    ).first()
    
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Table already booked for this time slot"
        )
    
    new_reservation = Reservation(
        user_id=current_user.id,
        table_id=reservation.table_id,
        start_time=reservation.start_time,
        end_time=reservation.end_time
    )
    
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    return new_reservation

@router.get("/", response_model=list[ReservationResponse])
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Reservation).filter(Reservation.user_id == current_user.id).all()

@router.delete("/{reservation_id}", status_code=status.HTTP_200_OK)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    if reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own reservations"
        )
    
    db.delete(reservation)
    db.commit()
    
    return {"message": "Reservation cancelled successfully"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.table import Table
from schemas.table_schema import TableCreate, TableResponse

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TableResponse)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    existing_table = db.query(Table).filter(Table.table_number == table.table_number).first()
    if existing_table:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Table number already exists"
        )
    
    new_table = Table(
        table_number=table.table_number,
        capacity=table.capacity
    )
    
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    
    return new_table

@router.get("/", response_model=list[TableResponse])
def get_all_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()
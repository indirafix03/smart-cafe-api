from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Table(Base):
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, unique=True, index=True)
    capacity = Column(Integer)
    is_available = Column(Boolean, default=True)
    
    reservations = relationship("Reservation", back_populates="table")
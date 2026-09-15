from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Molecule(Base):
    __tablename__ = "molecules"

    id = Column(Integer, primary_key=True, index=True)
    smiles = Column(String, nullable=False)
    canonical_smiles = Column(String, unique=True, nullable=False, index=True)
    mol_weight = Column(Float, nullable=True)
    formula = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
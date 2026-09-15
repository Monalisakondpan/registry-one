from pydantic import BaseModel
from datetime import datetime

class MoleculeCreate(BaseModel):
    smiles: str

class MoleculeResponse(BaseModel):
    id: int
    smiles: str
    canonical_smiles: str
    mol_weight: float
    formula: str
    created_at: datetime

    class Config:
        from_attributes = True
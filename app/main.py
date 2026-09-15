from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RegistryOne", description="Molecule Registration API")

@app.post("/molecules", response_model=schemas.MoleculeResponse, status_code=201)
def register_molecule(molecule: schemas.MoleculeCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_molecule(db, molecule.smiles)
    except ValueError as e:
        if "Duplicate" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/molecules/{molecule_id}", response_model=schemas.MoleculeResponse)
def read_molecule(molecule_id: int, db: Session = Depends(get_db)):
    molecule = crud.get_molecule(db, molecule_id)
    if molecule is None:
        raise HTTPException(status_code=404, detail="Molecule not found")
    return molecule

@app.get("/molecules", response_model=list[schemas.MoleculeResponse])
def list_molecules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_molecules(db, skip, limit)
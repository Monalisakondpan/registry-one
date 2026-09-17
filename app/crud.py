from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Molecule
from app.chem import canonicalize, get_properties

def create_molecule(db: Session, smiles: str) -> Molecule:
    canonical = canonicalize(smiles)

    existing = db.query(Molecule).filter(
        Molecule.canonical_smiles == canonical
    ).first()
    if existing:
        raise ValueError(f"Duplicate molecule. Matches existing ID {existing.id}")

    props = get_properties(smiles)

    molecule = Molecule(
        smiles=smiles,
        canonical_smiles=canonical,
        mol_weight=props["mol_weight"],
        formula=props["formula"],
    )
    db.add(molecule)
    db.commit()
    db.refresh(molecule)
    return molecule

def get_molecule(db: Session, molecule_id: int) -> Molecule | None:
    return db.query(Molecule).filter(Molecule.id == molecule_id).first()

def get_all_molecules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Molecule).offset(skip).limit(limit).all()

def search_similar_molecules(db: Session, smiles: str, threshold: float = 0.5):
    from app.chem import calculate_similarity
    all_molecules = db.query(Molecule).all()
    results = []
    for mol in all_molecules:
        similarity = calculate_similarity(smiles, mol.canonical_smiles)
        if similarity >= threshold:
            results.append((mol, similarity))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def delete_molecule(db: Session, molecule_id: int) -> bool:
    molecule = db.query(Molecule).filter(Molecule.id == molecule_id).first()
    if molecule is None:
        return False
    db.delete(molecule)
    db.commit()
    return True
    
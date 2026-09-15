from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

def canonicalize(smiles: str) -> str:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES string: {smiles}")
    return Chem.MolToSmiles(mol, canonical=True)

def get_properties(smiles: str) -> dict:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES string: {smiles}")
    return {
        "mol_weight": round(Descriptors.MolWt(mol), 2),
        "formula": rdMolDescriptors.CalcMolFormula(mol),
  }
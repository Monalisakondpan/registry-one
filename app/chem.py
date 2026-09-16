from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from rdkit import DataStructs
from rdkit.Chem import AllChem

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

def get_fingerprint(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES string: {smiles}")
    return AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)

def calculate_similarity(smiles1: str, smiles2: str) -> float:
    fp1 = get_fingerprint(smiles1)
    fp2 = get_fingerprint(smiles2)
    return DataStructs.TanimotoSimilarity(fp1, fp2)
from app.chem import canonicalize, get_properties, calculate_similarity

def test_canonicalize_returns_standard_form():
    assert canonicalize("OCC") == "CCO"

def test_canonicalize_same_molecule_different_notation():
    assert canonicalize("CCO") == canonicalize("OCC")

def test_canonicalize_invalid_smiles_raises():
    try:
        canonicalize("not_a_molecule")
        assert False, "Expected ValueError"
    except ValueError:
        pass

def test_get_properties_ethanol():
    props = get_properties("CCO")
    assert props["formula"] == "C2H6O"
    assert props["mol_weight"] == 46.07

def test_calculate_similarity_identical_molecules():
    assert calculate_similarity("CCO", "CCO") == 1.0

def test_calculate_similarity_different_molecules():
    similarity = calculate_similarity("CCO", "CCN")
    assert 0.0 < similarity < 1.0
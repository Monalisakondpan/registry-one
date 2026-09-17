import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_new_molecule():
    response = client.post("/molecules", json={"smiles": "c1ccccc1"})
    assert response.status_code in (201, 409)

def test_register_duplicate_returns_409():
    client.post("/molecules", json={"smiles": "CCN"})
    response = client.post("/molecules", json={"smiles": "NCC"})
    assert response.status_code == 409

def test_register_invalid_smiles_returns_500_or_422():
    response = client.post("/molecules", json={"smiles": "invalid###"})
    assert response.status_code in (422, 500)

def test_get_nonexistent_molecule_returns_404():
    response = client.get("/molecules/999999")
    assert response.status_code == 404

def test_list_molecules_returns_200():
    response = client.get("/molecules")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_molecules_find_similar():
    response = client.get("/molecules/search", params={"smiles": "CCO", "threshold": 0.1})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_molecule_removes_it():
    create_response = client.post("/molecules", json={"smiles": "c1ccncc1"})
    if create_response.status_code == 409:
        existing_id = int(create_response.json()["detail"].split()[-1])
        client.delete(f"/molecules/{existing_id}")
        create_response = client.post("/molecules", json={"smiles": "c1ccncc1"})

    molecule_id = create_response.json()["id"]

    delete_response = client.delete(f"/molecules/{molecule_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/molecules/{molecule_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_molecule_returns_404():
    response = client.delete("/molecules/999999")
    assert response.status_code == 404
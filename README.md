# RegistryOne

Molecule registration API demonstrating chemical structure canonicalization and duplicate detection at the data layer.


## What it does
- Registers molecules via SMILES notation
- Canonicalizes structures using RDKit - different notations of the same molecule are detected as duplicates
- Computes molecular weight and formula
- Exposes REST endpoints for registration, retrieval, and listing


## Stack
- Python, FastAPI
- PostgreSQL (Docker)
- SQLAlchemy ORM
- RDKit (cheminformatics)

## Endpoints
- `POST /molecules` - register a new molecule
- `GET /molecules/{id}` - fetch a molecule by ID
- `GET /molecules` - list molecules (paginated)

## Run locally
1. Start Postgres: `docker run --name registry-db -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=registry -p 5432:5432 -d postgres:16`
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `uvicorn app.main:app --reload`
4. Visit `http://127.0.0.1:8000/docs` for interactive API docs
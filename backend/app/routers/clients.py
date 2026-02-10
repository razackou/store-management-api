from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.crud.client import get_client, get_clients, create_client, update_client, delete_client

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=list[ClientRead])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_clients(db, skip, limit)

@router.get("/{client_id}", response_model=ClientRead)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/", response_model=ClientRead)
def create_new_client(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

@router.put("/{client_id}", response_model=ClientRead)
def update_existing_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    updated = update_client(db, client_id, client)
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated

@router.delete("/{client_id}", response_model=ClientRead)
def delete_existing_client(client_id: int, db: Session = Depends(get_db)):
    deleted = delete_client(db, client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")
    return deleted

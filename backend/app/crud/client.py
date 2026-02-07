from sqlalchemy.orm import Session
from app.models.clients import Client
from app.schemas.client import ClientCreate, ClientUpdate

def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()

def create_client(db: Session, client_data: ClientCreate):
    client = Client(**client_data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def update_client(db: Session, client_id: int, client_data: ClientUpdate):
    client = get_client(db, client_id)
    if not client:
        return None
    for key, value in client_data.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: int):
    client = get_client(db, client_id)
    if not client:
        return None
    db.delete(client)
    db.commit()
    return client

import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# ---------------------------------------------------------
# Force backend comme racine pour résoudre les imports app.*
# ---------------------------------------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base, get_db

# NOW import app after models are registered
from app.main import app

# Import all models FIRST to register them with Base


# ---------------------------------------------------------
# Fixture TestClient FastAPI with session and table creation
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def client():
    # Create in-memory SQLite database for this test
    # Use StaticPool to ensure all connections use the same in-memory database
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create session factory
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Override dependency
    app.dependency_overrides[get_db] = override_get_db

    # Create test client
    client = TestClient(app)

    yield client

    # Cleanup
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()  # Properly close all connections

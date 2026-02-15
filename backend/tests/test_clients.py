def test_crud_clients(client):
    # CREATE
    res = client.post("/clients/", json={"name": "Alice", "email": "alice@test.com"})
    assert res.status_code == 200
    client_id = res.json()["id"]

    # READ single
    res = client.get(f"/clients/{client_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Alice"

    # READ all
    res = client.get("/clients/")
    assert res.status_code == 200
    assert any(c["id"] == client_id for c in res.json())

    # UPDATE
    res = client.put(f"/clients/{client_id}", json={"name": "Alice Updated"})
    assert res.status_code == 200
    assert res.json()["name"] == "Alice Updated"

    # DELETE
    res = client.delete(f"/clients/{client_id}")
    assert res.status_code == 200
    res = client.get(f"/clients/{client_id}")
    assert res.status_code == 404

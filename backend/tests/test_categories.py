def test_crud_categories(client):
    # CREATE
    res = client.post("/categories/", json={"name": "Electronics"})
    assert res.status_code == 200
    cat_id = res.json()["id"]

    # READ
    res = client.get(f"/categories/{cat_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Electronics"

    # UPDATE
    res = client.put(f"/categories/{cat_id}", json={"name": "Electro"})
    assert res.status_code == 200
    assert res.json()["name"] == "Electro"

    # DELETE
    res = client.delete(f"/categories/{cat_id}")
    assert res.status_code == 200
    res = client.get(f"/categories/{cat_id}")
    assert res.status_code == 404

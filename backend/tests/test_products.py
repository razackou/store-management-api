def test_crud_products(client):
    # CREATE category first
    cat = client.post("/categories/", json={"name": "Books"}).json()
    cat_id = cat["id"]

    # CREATE product
    res = client.post(
        "/products/",
        json={
            "name": "Python Book",
            "description": "Learn Python",
            "unit_price": 29.99,
            "stock": 50,
            "category_id": cat_id,
        },
    )
    assert res.status_code == 200
    prod_id = res.json()["id"]

    # READ single
    res = client.get(f"/products/{prod_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Python Book"

    # UPDATE
    res = client.put(f"/products/{prod_id}", json={"stock": 45})
    assert res.status_code == 200
    assert res.json()["stock"] == 45

    # DELETE
    res = client.delete(f"/products/{prod_id}")
    assert res.status_code == 200
    res = client.get(f"/products/{prod_id}")
    assert res.status_code == 404

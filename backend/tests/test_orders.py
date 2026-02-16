def test_crud_orders(client):
    # CREATE client
    client_res = client.post(
        "/clients/", json={"name": "Alice", "email": "alice@zak.com"}
    ).json()
    client_id = client_res["id"]

    # CREATE employee
    emp_res = client.post("/employees/", json={"name": "Bob"}).json()
    emp_id = emp_res["id"]

    # CREATE category & product
    cat_id = client.post("/categories/", json={"name": "Gadgets"}).json()["id"]
    prod_res = client.post(
        "/products/",
        json={
            "name": "Gadget 1",
            "description": "Cool gadget",
            "unit_price": 19.99,
            "stock": 10,
            "category_id": cat_id,
        },
    ).json()
    prod_id = prod_res["id"]

    # CREATE order
    order_res = client.post(
        "/orders/",
        json={
            "client_id": client_id,
            "employee_id": emp_id,
            "status": "Pending",
            "products": [{"product_id": prod_id, "quantity": 2}],
        },
    )
    assert order_res.status_code == 200
    order_id = order_res.json()["id"]

    # READ single order
    res = client.get(f"/orders/{order_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["client_id"] == client_id
    assert data["status"] == "Pending"

    # READ all orders
    res = client.get("/orders/")
    assert res.status_code == 200
    assert any(o["id"] == order_id for o in res.json())

    # DELETE order
    res = client.delete(f"/orders/{order_id}")
    assert res.status_code == 200
    res = client.get(f"/orders/{order_id}")
    assert res.status_code == 404

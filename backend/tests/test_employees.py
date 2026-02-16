def test_crud_employees(client):
    # CREATE
    res = client.post(
        "/employees/", json={"name": "Zak", "position": "Cloud Architect"}
    )
    assert res.status_code == 200
    emp_id = res.json()["id"]

    # READ single
    res = client.get(f"/employees/{emp_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Zak"

    # READ all
    res = client.get("/employees/")
    assert res.status_code == 200
    assert any(e["id"] == emp_id for e in res.json())

    # UPDATE
    res = client.put(f"/employees/{emp_id}", json={"position": "Solution Architect"})
    assert res.status_code == 200
    assert res.json()["position"] == "Solution Architect"

    # DELETE
    res = client.delete(f"/employees/{emp_id}")
    assert res.status_code == 200
    res = client.get(f"/employees/{emp_id}")
    assert res.status_code == 404

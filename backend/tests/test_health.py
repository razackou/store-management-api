def test_health_endpoints(client):
    # liveness
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

    # DB readiness
    res = client.get("/health/db")
    assert res.status_code == 200
    assert res.json()["status"] == "database is up and running."

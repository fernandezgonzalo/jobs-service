from fastapi.testclient import TestClient
from app.main import app
from app.schemas import JobIn

client = TestClient(app)


def test_add_new_job():
    new_job = {
        "name": "python dev",
        "country": "Arg",
        "skills": [],
        "salary": 1
    }

    response = client.post("/add-job", json=new_job)
    assert response.status_code == 201



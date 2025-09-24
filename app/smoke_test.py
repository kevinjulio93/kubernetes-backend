from fastapi.testclient import TestClient
from .main import app


def run_smoke():
    # use context manager to ensure startup/shutdown events run
    with TestClient(app) as client:
        # create
        resp = client.post("/tasks", json={"name": "Test Task", "exec_time_seconds": 120, "notes": "smoke"})
        assert resp.status_code == 200, resp.text
        data = resp.json()
        task_id = data["id"]

        # list
        resp = client.get("/tasks")
        assert resp.status_code == 200, resp.text

        # update
        resp = client.put(f"/tasks/{task_id}", json={"status": "done"})
        assert resp.status_code == 200, resp.text

        # delete
        resp = client.delete(f"/tasks/{task_id}")
        assert resp.status_code == 200, resp.text

    print("smoke ok")


if __name__ == "__main__":
    run_smoke()

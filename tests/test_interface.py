from fastapi.testclient import TestClient

from interface.interface import app


client = TestClient(app)


def test_list_files_for_current_directory():
    response = client.post("/ls", json={"parameter": "",  "directory": ""})
    actual = response.json()
    expected = {"command": "ls",
                "files": ["README.md", "__pycache__", "core", "interface",
                          "logs", "model", "requirements.txt",
                          "server.py", "tests", "utils", "venv"]}
    assert actual == expected
    assert response.status_code == 200


def test_list_files_for_current_directory_with_parametes():
    response = client.post("/ls", json={"parameter": "-l", "directory": ""})
    assert response.status_code == 200


def test_list_files_when_directory_does_not_exist():
    response = client.post("/ls", json={"parameter": "-l",
                                        "directory": "/unknown/directory"})
    assert response.status_code == 404


def test_list_files_when_wrong_command_is_provided():
    response = client.post("/ls", json={"parameter": "-abc123",
                                        "directory": ""})
    assert response.status_code == 400


def test_when_command_is_not_implemented():
    response = client.post("/find", json="")
    assert response.status_code == 501


def test_any_route():
    response = client.post("/any", json={"command": "df",
                                         "parameter": "-h"})
    assert response.status_code == 200

from fastapi.testclient import TestClient

from interface.interface import app


client = TestClient(app)


def test_list_files_for_current_directory():
    response = client.post("/ls", json={"parameter": "ls",  "directory": ""})
    actual = response.json()
    expected = {"command": "ls",
                "files": ["README.md", "__pycache__", "core", "interface",
                          "logs", "model", "requirements.txt",
                          "server.py", "tests", "utils", "venv"]}
    assert actual == expected
    assert response.status_code == 200


def test_list_files_for_current_directory_with_parametes():
    response = client.post("/ls", json={"parameter": "ls -l", "directory": ""})
    assert response.status_code == 200


def test_list_files_when_directory_does_not_exist():
    response = client.post("/ls", json={"parameter": "ls -l",
                                        "directory": "/unknown/directory"})
    actual = response.text
    expected = "Ops! Sorry no such file or directory."
    assert actual == expected
    assert response.status_code == 404


def test_list_files_when_wrong_command_is_provided():
    response = client.post("/ls", json={"parameter": "ls -abc123",
                                        "directory": ""})
    actual = response.text
    expected = "Ops! Sorry wrong command entered."
    assert actual == expected
    assert response.status_code == 400


def test_when_command_is_not_implemented():
    response = client.post("/ls", json={"parameter": "echo",
                                        "directory": "Hello World"})
    actual = response.text
    expected = "Command not yet implemented."
    assert actual == expected
    assert response.status_code == 501

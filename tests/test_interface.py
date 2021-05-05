from fastapi.testclient import TestClient

from interface.interface import app


client = TestClient(app)


def test_echo():
    response = client.post("/echo",
                           json={"command": "echo",
                                 "message": "Hello World!"})

    actual = response.json()
    expected = {'command': 'echo Hello World!',
                'output': 'Hello World!'}

    assert actual == expected


def test_list_files_for_present_directory():
    response = client.post("/list-files",
                           json={"command": "ls",
                                 "directory": ""})
    actual = response.json()
    expected = {'command': 'ls ',
                'output': ['README.md', '__pycache__', 'core', 'interface',
                           'logs', 'model', 'requirements.txt', 'server.py',
                           'tests', 'utils', 'venv', '']}

    assert actual == expected


def test_list_files_when_directory_does_not_exist():
    response = client.post("/list-files",
                           json={"command": "ls",
                                 "directory": "/unknown/directory"})
    actual = response.json()
    expected = {'error': 'ls: /unknown/directory: No such file or directory'}

    assert actual == expected


def test_list_files_when_no_input_is_provided():
    response = client.post("/list-files",
                           json={"command": "",
                                 "directory": ""})
    actual = response.json()
    expected = {'error': 'no input provided'}

    assert actual == expected

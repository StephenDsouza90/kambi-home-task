# Kambi Home Task

This repo represents the home task of Kambi. The task were as follows:

1. Build an API with a JSON payload
2. The API will make a call to an arbitrary external executable
3. New requests should be handled while performing a blocking call
4. There should be a graceful shutdown if SIGINT is sent to the API
5. Handle custom messages for 400, 404, 500, 501, etc.
6. Write sample unit test(s)

## Virtual Environment and Dependencies

To start using the application, create a virtual environment and install the dependencies.

Run the following commands:

To create a virtual environment
```bash
>> python3.6 -m venv venv
```

To activate the virtual environment

|Platform   |Command                                  |
|-----------|-----------------------------------------|
|Mac        |```$ source venv/bin/activate```         |
|           |```$ . venv/bin/activate.fish```         |
|           |```$ source venv/bin/activate.csh```     |
|Windows    |```C:\> venv\Scripts\activate.bat```     |
|           |```PS C:\> venv\Scripts\Activate.ps1```  |


To install the dependencies
```bash
>> pip install -r requirements.txt
```

## Starting the Server

The API is built with [FastApi](https://fastapi.tiangolo.com/) and the Server is [Gunicorn]("https://gunicorn.org/").

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+. It can also be used to write Asynchronous coding within Python.

Gunicorn server is a production-ready server.

To start running the server, run the following command.

```bash
>> gunicorn server:app --graceful-timeout 120 -w 4 -k uvicorn.workers.UvicornWorker -p app.pid
```

- --graceful-timeout 120 (TODO : Write what does this mean)
- -w 4 (TODO : Write what does this mean)
- -k uvicorn.workers.UvicornWorker (TODO : Write what does this mean)
-p app.pid (TODO : Write what does this mean)

## Swagger UI

The best way to send data to the API is by using the Swagger UI that is provided from FastAPI.

Enter the below URL on a browser.

```bash
http://127.0.0.1:8000/docs
```

## Curl commands

Curl commands can be used as follows:

For echo

```bash
>> curl -X 'POST' 'http://127.0.0.1:8080/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"command": "echo", "message": "<message>"}'
```

For list files from a directory

```bash
>> curl -X 'POST' 'http://127.0.0.1:8080/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"command": "ls", "directory": "<directory>"}'
```

## Implementation

The app is built using Python and the routes are created using FastAPI. The API routes accepts JSON structure data as a payload. The app is also written with asynchronous coding using async/await keywords. 

### API and Executables

The available routes are:

- /echo
- /list-files

These routes are mapped to methods which execute a command in a terminal.

The `/echo` route will trigger a `echo <message>`. The `/list-files` route will trigger a `ls <path>`.

The results from these commands will be saved in a dict and then a response will be returned to the user.

### Blocking Call
To simulate a blocking call, the `asyncio.sleep()` is used. By using `asyncio.sleep()` this becomes a non-blocking call and allows the api to accept more requests to perform other task. However, when the `time.sleep()` is used, a api waits until a process is finished.

More information can be found [here](https://stackoverflow.com/questions/56729764/python-3-7-asyncio-sleep-and-time-sleep)

### Graceful Shutdown

To shutdown the server in a graceful way, the `kill` command can be used from another terminal.

The `kill` command sends the specified signal to the specified processes or process groups.

In this app, the process id is saved in the app.pid file when the server is running.

To kill the process, run the following command:

```bash
>> kill -15 <process_id>
```

If in case any requests are in process, then the server will shutdown after the requests have been completed.

```bash
2021-05-05 17:37:55,680 - kambi_home_task - INFO - Starting server
2021-05-05 17:37:55,681 - kambi_home_task - INFO - Listening at: http://127.0.0.1:8000
2021-05-05 17:38:35,319 - kambi_home_task - INFO - {'command': 'ls ', 'output': ['README.md', '__pycache__', 'app.pid', 'core', 'interface', 'logs', 'model', 'requirements.txt', 'server.py', 'tests', 'utils', 'venv', '']}
2021-05-05 17:38:37,400 - kambi_home_task - INFO - {'command': 'echo hello', 'output': 'hello'}
2021-05-05 17:38:37,411 - kambi_home_task - INFO - Application shutdown after completing all requests
```

### Custom Messages

Custom messages are logged in the logs/api.log folder.

### Tests

To run the test cases, run the following command:

```bash
pytest -vv

============================================================================ test session starts =============================================================================
platform darwin -- Python 3.6.8, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /Users/stedsou/Documents/Stephen/kambi_home_task/kambi-home-task/venv/bin/python3.6
cachedir: .pytest_cache
rootdir: /Users/stedsou/Documents/Stephen/kambi_home_task/kambi-home-task
collected 4 items


tests/test_interface.py::test_echo PASSED                                                                                                                              [ 25%]
tests/test_interface.py::test_list_files_for_present_directory PASSED                                                                                                  [ 50%]
tests/test_interface.py::test_list_files_when_directory_does_not_exist PASSED                                                                                          [ 75%]
tests/test_interface.py::test_list_files_when_no_input_is_provided PASSED                                                                                              [100%]

============================================================================= 4 passed in 15.32s =============================================================================
```

# Kambi Home Task

This repository represents the Kambi home task.

The task are as follows:

1. Build an API with a JSON payload.
2. The API will make a call to an arbitrary external executable.
3. New requests should be handled while performing a blocking call.
4. There should be a graceful shutdown if SIGINT is sent to the API.
5. Handle custom messages for 400, 404, 500, 501.
6. Write sample unit test(s).

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

The API is built with [FastAPI](https://fastapi.tiangolo.com/) and the Server is [Gunicorn]("https://gunicorn.org/").

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+. It can also be used to write asynchronous coding within Python.

Gunicorn server is a production-ready server.

To start running the server, run the following command.

```bash
>> gunicorn server:app --graceful-timeout 120 -w 4 -k uvicorn.workers.UvicornWorker -p app.pid
```
- **gunicorn**: Server being used.
- **server:app**: Entry point of the application.
- **--graceful-timeout 120**: Amount of time for the shutdown to take place once the kill signal is received.
- **-w 4**: Workers handling the requests.
- **-k uvicorn.workers.UvicornWorker**: Type of workers
- **-p app.pid**: Process ID (ID will be saved in the app.pid file which will be created on the fly)

## Interacting with the API
### Swagger UI

The best way to use the API is via the Swagger UI that is provided by FastAPI.

Enter the below URL on a browser.

```bash
http://127.0.0.1:8000/docs
```

The JSON payload

```json
{
    "parameter": "ls",
    "directory": ""
}
```

### Curl commands

Another way to interact with the API is by entering a curl command in a separate terminal.

Curl commands can be used as follows:

```bash
>> curl -X 'POST' 'http://127.0.0.1:8000/ls' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"parameter": "ls", "directory": ""}'
```

<details>
<summary>Result</summary>

```json
{
    "command": "ls",
    "files":["README.md",
            "__pycache__",
            "core",
            "interface",
            "logs",
            "model",
            "requirements.txt",
            "server.py",
            "tests",
            "utils",
            "venv"]
}
```

</details>

## Implementation of the task

The app is written in Python Programming Language and the API is built using FastAPI. This app is also written with asynchronous coding using async/await keywords.

### API and Executables

The `/ls` route accepts JSON structure data as a payload. The route is mapped to function which will execute a command in a terminal. However, the result will not be printed in the terminal but rather saved in a variable so that the response can be sent back to the user.

The JSON structure contains two keys:
- parameter: where a user can provides commands such as `ls`or `ls -l`or any other valid `ls`parameter.
- directory: where a user specifies a directory for which they want the list of files. If no directory is provided then a default directory is used.

A response with the result will be sent to the user. If in case there are any errors then a custom message will be sent to the user.

### Blocking Call

To simulate a blocking call, the `time.sleep()` is used. Any function that calls the `blocking_call()`, that process will sleep for 5 seconds. The `blocking_call()` itself is an asynchronous function which mean it will pass on control to any other function while the `blocking_call()` function is sleeping.

In order to simulate a non-blocking call, the `asyncio.sleep()` can be used. More information can be found [here](https://stackoverflow.com/questions/56729764/python-3-7-asyncio-sleep-and-time-sleep)

### Graceful Shutdown

To shutdown the server in a graceful way, the `kill` command can be used from another terminal. The `kill` command sends the specified signal to the specified processes or process groups. In this app, the `process_id` is saved in the app.pid file when the server is running.

To kill the process, run the following command:

```bash
>> kill -15 <process_id>
```

If in case any requests are in process, then the server will shutdown after the requests have been completed. This process can be viewed in the terminal running the server or in the log file.

### Custom Messages

If there are any errors then a custom message and the appropriate status code will be sent to the user.

Currently the supported status code are:

- HTTP_400_BAD_REQUEST: Ops! Sorry wrong command entered.
- HTTP_404_NOT_FOUND: Ops! Sorry no such file or directory.
- HTTP_500_INTERNAL_SERVER_ERROR: Ops! Something went wrong.
- HTTP_501_NOT_IMPLEMENTED: Command not yet implemented.

These messages are logged in the logs/api.log.

## Tests

To run the test cases, run the following command:

```bash
>> pytest -vv
```

```bash
======================================================================================================= test session starts =======================================================================================================
platform darwin -- Python 3.6.8, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /Users/stedsou/Documents/Stephen/kambi_home_task/kambi-home-task/venv/bin/python3.6
cachedir: .pytest_cache
rootdir: /Users/stedsou/Documents/Stephen/kambi_home_task/kambi-home-task
collected 5 items

tests/test_interface.py::test_list_files_for_current_directory PASSED                                                                                                                                                       [ 20%]
tests/test_interface.py::test_list_files_for_current_directory_with_parametes PASSED                                                                                                                                        [ 40%]
tests/test_interface.py::test_list_files_when_directory_does_not_exist PASSED                                                                                                                                               [ 60%]
tests/test_interface.py::test_list_files_when_wrong_command_is_provided PASSED                                                                                                                                              [ 80%]
tests/test_interface.py::test_when_command_is_not_implemented PASSED                                                                                                                                                        [100%]

======================================================================================================= 5 passed in 10.54s ========================================================================================================
```

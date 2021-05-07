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

By default, `ls` will be used and a user can provide additional parameters.

```json
{
    "parameter": "-l",
    "directory": "/Users/stedsou/kambi-home-task"
}
```

### Curl commands

Another way to interact with the API is by entering a curl command in a separate terminal.

Curl commands can be used as follows:

```bash
>> curl -X 'POST' 'http://127.0.0.1:8000/ls' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"parameter": "-l", "directory": "/Users/stedsou/kambi-home-task"}'
```

<details>
<summary>Result</summary>

```json
{
  "command": "ls -l /Users/stedsou/kambi-home-task",
  "files": [
    "total 40",
    "-rw-r--r--@ 1 stedsou  58041779  7558  7 May 17:14 README.md",
    "drwxr-xr-x  4 stedsou  58041779   128  5 May 16:41 __pycache__",
    "-rw-r--r--  1 stedsou  58041779     6  7 May 17:13 app.pid",
    "drwxr-xr-x  4 stedsou  58041779   128  7 May 17:04 core",
    "drwxr-xr-x  4 stedsou  58041779   128  7 May 16:59 interface",
    "drwxr-xr-x  3 stedsou  58041779    96  7 May 00:57 logs",
    "drwxr-xr-x  4 stedsou  58041779   128  7 May 16:59 model",
    "-rw-r--r--  1 stedsou  58041779   518  5 May 16:52 requirements.txt",
    "-rw-r--r--  1 stedsou  58041779   280  5 May 16:41 server.py",
    "drwxr-xr-x  5 stedsou  58041779   160  7 May 17:08 tests",
    "drwxr-xr-x  4 stedsou  58041779   128  7 May 10:37 utils",
    "drwxr-xr-x  6 stedsou  58041779   192  2 May 17:09 venv"
  ]
}
```

</details>

## Implementation of the task

The app is written in Python Programming Language and the API is built using FastAPI. This app is also written with asynchronous coding using AsyncIO framework.

### API and Executables

The `/ls` route accepts JSON structure data as a payload. The route is mapped to function which will execute a command in a terminal. This will call the ls command, parse the output and return it back to the client in JSON format.

The input JSON structure contains two keys:
- parameter: where a user can provides commands such as `-l`, `-alh` or any other valid `ls`parameter.
- directory: where a user specifies a directory for which they want the list of files. If no directory is provided then a default directory is used.

A response with the result will be sent to the user. If in case there are any errors then a custom message will be sent to the user.

### Blocking Call

To simulate a blocking call, the `time.sleep()` is used. Any function that calls the `blocking_call()` will execute the `sleep()` command, but AsyncIO event loop will recognize it and switch context to another thread to continue taking on new requests. The `blocking_call()` is made an asynchronous by setting the async keyword to the function which mean it will pass on control to any other function upon the blocking call to not block the process.

Alternatively, one could also use `asyncio.sleep()` instead.

### Graceful Shutdown

To shutdown the server in a graceful way, the `kill` command can be used. The `kill` command can send the TERM or 15 signal to the process telling the application it needs to prepare to shutdown. In this app, the `process_id` is saved in the app.pid file when the server is running.

To kill the process, run the following command:

```bash
>> kill -15 <process_id>
```

If in case any requests are in flight, then the server will shutdown after the requests in flight have been completed. This process can be viewed in the terminal running the server or in the log file.

**Sample log**

```bash
[2021-05-07 17:31:38 +0200] [56051] [INFO] Waiting for application shutdown.
[2021-05-07 17:31:38 +0200] [56051] [INFO] Application shutdown complete.
[2021-05-07 17:31:38 +0200] [56051] [INFO] Finished server process [56051]
[2021-05-07 17:31:38 +0200] [56051] [INFO] Worker exiting (pid: 56051)
[2021-05-07 17:31:38 +0200] [56045] [INFO] Shutting down: Master
```

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

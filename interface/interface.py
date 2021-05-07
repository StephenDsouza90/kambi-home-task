import logging

from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse

from core.core import list_files_executable
from model.model import ListFiles


app = FastAPI()
app.title = "Kambi Home Task!"
app.description = "This is the home task for Kambi."

logger = logging.getLogger("kambi_home_task")


@app.get("/")
def index():
    return {"message": "Welcome to the Kambi Home Task. Please navigate to /docs to use the swagger UI."}


@app.post("/ls", tags=["Kambi"])
async def list_files(executable: ListFiles):
    """
    Route for the "ls" command which accepts JSON data in the request.
    The values are saved in the executable.

    :param executable: Object containing command, parameter and directory from the user.
    :return response: Custom response for the user.
    """
    response = await list_files_executable(executable)
    return response


@app.on_event("shutdown")
def shutdown_event():
    """
    Handles shutdown if there is a SIGINT sent to the server.
    A log is created after the shutdown has been completed.

    To send a SIGINT, run the following command in a terminal.
    >> kill -15 <process_id>
    """
    logger.info("Application shutdown after completing all requests")


@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    """
    Handles any exception if there is an error in the code.
    A custom response is sent to the user.
    A log with the error is created.
    """
    logger.info(exc)
    return PlainTextResponse(f"Ops! Something went wrong.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

import logging

from fastapi import FastAPI

from core.core import list_files_executable, echo_executable
from model.model import ListFiles, Echo


app = FastAPI()
app.title = "Kambi Home Task!"
app.description = "This is the home task for Kambi."


@app.get("/")
def index():
    """
    """

    return {"message": "Welcome to the Kambi Home Task. Please navigate to /docs"}


@app.post("/list-files", tags=["Kambi"])
async def list_files(executable: ListFiles):
    """
    """

    response = await list_files_executable(executable)
    return response


@app.post("/echo", tags=["Kambi"])
async def echo(executable: Echo):
    """
    """

    response = await echo_executable(executable)
    return response


@app.on_event("shutdown")
def shutdown_event():
    """
    """

    logger = logging.getLogger("kambi_home_task")
    logger.info("Application shutdown after completing all requests")

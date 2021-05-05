import asyncio
import logging

from model.model import ListFiles, Echo
from utils.utils import pipe_open, error_response, list_files_successful_response, echo_successful_response


logger = logging.getLogger("kambi_home_task")


async def echo_executable(executable: Echo):
    """
    """

    if executable.command == "" and executable.message == "":
        response = error_response("no input provided in /echo")
        logger.error(response)
    else:
        if executable.message != "":
            complete_list = [executable.command, executable.message]
        else:
            complete_list = [executable.command]

        await blocking_call()

        output, error = pipe_open(complete_list)

        if output:
            response = echo_successful_response(executable.command,
                                                output.decode("utf-8").replace("\n", ""))
            logger.info(response)
        elif error:
            response = error_response(error)
            logger.error(response)

    return response


async def list_files_executable(executable: ListFiles):
    """
    """

    if executable.command == "" and executable.directory == "":
        response = error_response("no input provided in /list-files")
        logger.error(response)
    else:
        command_list = executable.command.split(" ")

        if executable.directory != "":
            # Any other directory
            complete_list = command_list + [executable.directory]
        else:
            # Current directory
            complete_list = command_list

        await blocking_call()

        output, error = pipe_open(complete_list)

        if output:
            files_in_dir = convert_bytes_to_list(output)
            response = list_files_successful_response(executable.directory,
                                                      executable.command,
                                                      files_in_dir)
            logger.info(response)
        elif error:
            response = error_response(error.decode("utf-8").replace("\n", ""))
            logger.error(response)

    return response


async def blocking_call():
    """
    Blocking call
    time.sleep(5)
    """
    await asyncio.sleep(20)


def convert_bytes_to_list(result_in_bytes):
    """
    """
    files_in_dir = result_in_bytes.decode("utf-8").split("\n")
    return files_in_dir

import time
import logging
import re

from fastapi import status
from fastapi.responses import PlainTextResponse

from model.model import ListFiles, Any

from utils.utils import (decode_byte_value, pipe_open, get_additional_parameters,
                         get_directory, get_response, get_all_commands,
                         get_command_list_with_param)


logger = logging.getLogger("kambi_home_task")


async def list_files_executable(executable: ListFiles):
    """
    If command "ls" and parameter (Optional) "-l" is provided but no directory is provided
    then by default, the current directory's files will be listed. Otherwise, if a directory is provided
    then that directory's files will be listed.

    The command with parameter (if any) along with the directory (if any) will be processed.
    Output or error will be returned instead of being printed in the terminal.

    If the returned output is successful, then the list of files will be sent to the user.
    If there is an error, then a custom response and status code will be sent to the user.

    Additionally, if there is a command besides ls or if there is any error in the code
    then a 501 or 500 will be sent to the user along with a custom message.

    All responses are logged in the api.log file in the logs folder.

    To stimulate a blocking call, a time.sleep() is used which is an asynchronous function.

    :param executable: Object containing command, parameter and directory from the user.
    :return response: Custom response for the user.
    """

    # ls command
    list_file_command = ["ls"]

    # Additional parameters
    list_file_command = get_additional_parameters(executable,
                                                  list_file_command)

    # Another dir (if any)
    list_file_command = get_directory(executable, list_file_command)

    # Executes a command in a terminal but returns an output or error which is saved in a variable
    output, error = await get_output_or_error(list_file_command)

    if error:
        # When a parameter in a command is not valid
        if re.search(pattern="illegal option", string=decode_byte_value(error), flags=re.I):
            logger.error(error)
            return PlainTextResponse("Ops! Sorry wrong command entered.", status_code=status.HTTP_400_BAD_REQUEST)
        # When a dir or file does not exist
        elif re.search(pattern="No such file or directory", string=decode_byte_value(error), flags=re.I):
            logger.error(error)
            return PlainTextResponse("Ops! Sorry no such file or directory.", status_code=status.HTTP_404_NOT_FOUND)

    # Simulate blocking call
    await blocking_call()

    response = get_response(output, list_file_command)
    return response


async def any_executable(executable: Any):
    """
    This is a function that handles any command that a user will provide.
    """

    command_list = get_all_commands(executable)
    command_list_with_param = get_command_list_with_param(executable,
                                                          command_list)

    output, error = await get_output_or_error(command_list_with_param)

    if error:
        if re.search(pattern="illegal option", string=decode_byte_value(error), flags=re.I):
            logger.error(error)
            return PlainTextResponse("Ops! Sorry wrong command entered.", status_code=status.HTTP_400_BAD_REQUEST)

    response = get_response(output, command_list_with_param)
    return response


async def blocking_call():
    """
    Stimulates a blocking call.
    To stimulates a non-blocking call, asyncio.sleep() can be used alternatively.
    """
    time.sleep(5)


async def get_output_or_error(commands: list):
    try:
        output, error = pipe_open(commands)
        return output, error
    except:
        return PlainTextResponse(f"Ops! Something went wrong.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

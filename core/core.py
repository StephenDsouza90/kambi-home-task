import time
import logging
import re

from fastapi import status
from fastapi.responses import PlainTextResponse

from model.model import ListFiles, Any

from utils.utils import (success_response, decode_byte_value,
                         convert_bytes_to_list, pipe_open)


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
    list_file_command = _get_additional_parameters(executable,
                                                   list_file_command)

    # Another dir (if any)
    list_file_command = _get_directory(executable, list_file_command)

    # Executes a command in a terminal but returns an output or error which is saved in a variable
    output, error = _get_output_or_error(list_file_command)

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

    files_in_dir = convert_bytes_to_list(output)
    response = success_response(" ".join(list_file_command), files_in_dir)
    logger.info(response)

    return response


async def any_executable(executable: Any):

    command_list = _get_all_commands(executable)
    command_list_with_param = _get_command_list_with_param(executable,
                                                           command_list)

    output, error = _get_output_or_error(command_list_with_param)

    if error:
        if re.search(pattern="illegal option", string=decode_byte_value(error), flags=re.I):
            logger.error(error)
            return PlainTextResponse("Ops! Sorry wrong command entered.", status_code=status.HTTP_400_BAD_REQUEST)

    result = convert_bytes_to_list(output)
    response = success_response(" ".join(command_list_with_param), result)
    return response


async def blocking_call():
    """
    Stimulates a blocking call.
    To stimulates a non-blocking call, asyncio.sleep() can be used alternatively.
    """
    time.sleep(5)


def _get_additional_parameters(executable: ListFiles, list_file_command: list):
    parameter = executable.parameter
    if parameter != "":
        list_file_command.append(parameter)
    return list_file_command


def _get_directory(executable: ListFiles, list_file_command: list):
    directory = executable.directory
    if directory != "":
        list_file_command.append(directory)
    return list_file_command


def _get_output_or_error(commands: list):
    try:
        output, error = pipe_open(commands)
        return output, error
    except:
        return PlainTextResponse(f"Ops! Something went wrong.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_all_commands(executable: Any):
    command = executable.command
    if " " in command:
        command_list = command.split(" ")
    else:
        command_list = [command]
    return command_list


def _get_command_list_with_param(executable: Any, command_list: list):
    parameters = executable.parameter
    if parameters == "":
        command_list_with_param = command_list
    else:
        command_list_with_param = command_list + [parameters]
    return command_list_with_param

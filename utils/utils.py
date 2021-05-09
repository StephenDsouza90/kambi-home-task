import logging
from logging.handlers import TimedRotatingFileHandler
from subprocess import Popen, PIPE

from model.model import ListFiles, Any

logger = logging.getLogger("kambi_home_task")


def pipe_open(commands: list):
    """
    A command is sent to the terminal which then returns an output or an error which is saved in a variable.

    :param commands: A complete list of commands sent to the terminal
    :return output: An output containing the list of files (if successful)
    :return error: An error containing the error response (if unsuccessful)
    """
    process = Popen(commands, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    return output, error


def success_response(command: str, files: list):
    return {"command": command, "files": files}


def initialize_logging(file_path: str, logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    file_handler = TimedRotatingFileHandler(file_path, when='midnight',
                                            interval=1)
    file_handler.suffix = '%Y%m%d'
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def decode_byte_value(value: str):
    return value.decode("utf-8").replace("\n", "")


def convert_bytes_to_list(result_in_bytes: bytes):
    return result_in_bytes.decode("utf-8").strip().split("\n")


def get_directory(executable: ListFiles, list_file_command: list):
    directory = executable.directory
    if directory != "":
        list_file_command.append(directory)
    return list_file_command


def get_additional_parameters(executable: ListFiles, list_file_command: list):
    parameter = executable.parameter
    if parameter != "":
        list_file_command.append(parameter)
    return list_file_command


def get_all_commands(executable: Any):
    command = executable.command
    if " " in command:
        command_list = command.split(" ")
    else:
        command_list = [command]
    return command_list


def get_command_list_with_param(executable: Any, command_list: list):
    parameters = executable.parameter
    if parameters == "":
        command_list_with_param = command_list
    else:
        command_list_with_param = command_list + [parameters]
    return command_list_with_param


def get_response(output, commands):
    result = convert_bytes_to_list(output)
    response = success_response(" ".join(commands), result)
    logger.info(response)
    return response

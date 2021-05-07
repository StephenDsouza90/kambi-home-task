import logging
from logging.handlers import TimedRotatingFileHandler
from subprocess import Popen, PIPE


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

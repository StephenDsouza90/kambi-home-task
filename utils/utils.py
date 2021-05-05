import logging
from logging.handlers import TimedRotatingFileHandler
from subprocess import Popen, PIPE


def pipe_open(complete_list):
    process = Popen(complete_list, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    return output, error


def list_files_successful_response(directory, command, files):
    response = {
        "command": f"{command} {directory}",
        "output": files
    }
    return response


def echo_successful_response(command, message):
    response = {
        "command": f"{command} {message}",
        "output": message
    }
    return response


def error_response(error):
    response = {"error": error}
    return response


def initialize_logging(file_path: str, logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    file_handler = TimedRotatingFileHandler(
        file_path, when='midnight', interval=1)
    file_handler.suffix = '%Y%m%d'
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

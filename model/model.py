from pydantic import BaseModel


class Command(BaseModel):
    """
    """

    command: str = ""


class ListFiles(Command):
    """
    """

    directory: str = ""


class Echo(Command):
    """
    """

    message: str = ""

from pydantic import BaseModel


class ListFiles(BaseModel):
    """ Represents the list file properties """

    parameter: str = ""
    directory: str = ""

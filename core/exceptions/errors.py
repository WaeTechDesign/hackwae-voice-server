"""
HackWae Voice Server

Custom Exceptions
"""


class NotFoundError(Exception):

    def __init__(

        self,

        message: str,

    ):

        self.message = message


# --------------------------------------------------


class BadRequestError(Exception):

    def __init__(

        self,

        message: str,

    ):

        self.message = message


# --------------------------------------------------


class ConflictError(Exception):

    def __init__(

        self,

        message: str,

    ):

        self.message = message

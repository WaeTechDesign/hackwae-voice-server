"""
HackWae Voice Server

Success Response
"""


def success(

    *,

    data=None,

    message: str | None = None,

    **extra,

):

    response = {

        "success": True,

    }

    if message is not None:

        response["message"] = message

    if data is not None:

        response["data"] = data

    response.update(extra)

    return response

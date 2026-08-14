"""
HackWae Voice Server

Created Response
"""

from fastapi.responses import JSONResponse


def created(

    *,

    data=None,

    message="Created",

):

    body = {

        "success": True,

        "message": message,

    }

    if data is not None:

        body["data"] = data

    return JSONResponse(

        status_code=201,

        content=body,

    )

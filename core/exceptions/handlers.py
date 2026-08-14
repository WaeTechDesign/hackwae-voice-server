"""
HackWae Voice Server

Exception Handlers
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .errors import (
    BadRequestError,
    ConflictError,
    NotFoundError,
)


def register_handlers(

    app: FastAPI,

):

    # ------------------------------------------

    @app.exception_handler(NotFoundError)
    async def not_found(

        request,

        exc: NotFoundError,

    ):

        return JSONResponse(

            status_code=404,

            content={

                "success": False,

                "message": exc.message,

            },

        )

    # ------------------------------------------

    @app.exception_handler(BadRequestError)
    async def bad_request(

        request,

        exc: BadRequestError,

    ):

        return JSONResponse(

            status_code=400,

            content={

                "success": False,

                "message": exc.message,

            },

        )

    # ------------------------------------------

    @app.exception_handler(ConflictError)
    async def conflict(

        request,

        exc: ConflictError,

    ):

        return JSONResponse(

            status_code=409,

            content={

                "success": False,

                "message": exc.message,

            },

        )

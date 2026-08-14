"""
HackWae Voice Server

History Route
"""

from fastapi import APIRouter
from fastapi.responses import FileResponse

from core.exceptions.errors import NotFoundError
from core.responses.success import success

from services.history_service import history_service

router = APIRouter()


# --------------------------------------------------

@router.get("/")
def history():

    return success(

        data=history_service.list(),

    )


# --------------------------------------------------

@router.get("/{filename}")
def download(filename: str):

    file = history_service.get(filename)

    if file is None:

        raise NotFoundError(

            "History file not found."

        )

    return FileResponse(

        path=file,

        filename=file.name,

        media_type="audio/wav",

    )


# --------------------------------------------------

@router.delete("/{filename}")
def delete(filename: str):

    if not history_service.delete(filename):

        raise NotFoundError(

            "History file not found."

        )

    return success(

        message="History deleted successfully.",

    )


# --------------------------------------------------

@router.delete("/")
def clear():

    history_service.clear()

    return success(

        message="History cleared.",

    )

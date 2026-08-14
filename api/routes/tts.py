"""
HackWae Voice Server

TTS Route
"""

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

from core.exceptions.errors import (
    BadRequestError,
    NotFoundError,
)

from core.responses.success import success

from schemas.request import TTSRequest

from services.engine_service import engine_service
from services.queue.manager import queue_manager
from services.voice_service import voice_service


router = APIRouter()


# ==================================================
# CREATE TTS JOB
# ==================================================


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
)
def tts(
    request: TTSRequest,
):

    # ----------------------------------------------
    # Normalize
    # ----------------------------------------------

    text = request.text.strip()

    voice = request.voice.strip()

    engine = request.engine.strip().lower()

    # ----------------------------------------------
    # Text validation
    # ----------------------------------------------

    if not text:

        raise BadRequestError(

            "Text tidak boleh kosong."

        )

    # ----------------------------------------------
    # Engine validation
    # ----------------------------------------------

    if not engine_service.exists(

        engine

    ):

        raise NotFoundError(

            f"Engine '{engine}' tidak ditemukan."

        )

    # ----------------------------------------------
    # Voice validation
    # ----------------------------------------------

    if voice_service.get(

        voice

    ) is None:

        raise NotFoundError(

            f"Voice '{voice}' tidak ditemukan."

        )

    # ----------------------------------------------
    # Output validation
    # ----------------------------------------------

    output = request.output

    if output is not None:

        output = output.strip()

        if not output:

            output = None

        elif (

            "/" in output

            or "\\" in output

        ):

            raise BadRequestError(

                "Output hanya boleh berupa "
                "nama file."

            )

        elif not output.lower().endswith(

            ".wav"

        ):

            raise BadRequestError(

                "Output file harus menggunakan "
                "format WAV."

            )

    # ----------------------------------------------
    # Create queue job
    # ----------------------------------------------

    job = queue_manager.create(

        text=text,

        voice=voice,

        engine=engine,

        output=output,

    )

    # ----------------------------------------------
    # Response
    # ----------------------------------------------

    return JSONResponse(

        status_code=status.HTTP_202_ACCEPTED,

        content=success(

            message="TTS job queued.",

            data={

                "job_id": job.id,

                "status": job.status,

            },

        ),

    )

"""
HackWae Voice Server

Upload Route
"""

from pathlib import Path
from tempfile import NamedTemporaryFile
import zipfile

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException

from core.exceptions.errors import BadRequestError

from core.responses.success import success

from services.upload.model import model_upload
from services.upload.voice import voice_upload


router = APIRouter()


VOICE_MAX_SIZE = 100 * 1024 * 1024

MODEL_MAX_SIZE = 10 * 1024 * 1024 * 1024


# ==================================================
# VOICE
# ==================================================


@router.post("/voice")
async def upload_voice(

    file: UploadFile = File(...),

):

    if not file.filename:

        raise BadRequestError(

            "Upload file tidak memiliki nama."

        )

    if not file.filename.lower().endswith(

        ".zip"

    ):

        raise BadRequestError(

            "Voice package harus berupa file ZIP."

        )

    temp_file = None

    total_size = 0

    try:

        temp_file = NamedTemporaryFile(

            delete=False,

            suffix=".zip",

        )

        while True:

            chunk = await file.read(

                1024 * 1024

            )

            if not chunk:

                break

            total_size += len(chunk)

            if total_size > VOICE_MAX_SIZE:

                raise BadRequestError(

                    "Ukuran voice package "
                    "melebihi batas 100 MB."

                )

            temp_file.write(chunk)

        temp_file.close()

        manifest = voice_upload.upload_zip(

            Path(temp_file.name)

        )

        return success(

            message=(
                "Voice uploaded successfully."
            ),

            data=manifest.model_dump(),

        )

    except FileExistsError as exc:

        raise HTTPException(

            status_code=409,

            detail=str(exc),

        )

    except zipfile.BadZipFile:

        raise BadRequestError(

            "File ZIP tidak valid atau rusak."

        )

    except ValueError as exc:

        raise BadRequestError(

            str(exc)

        )

    finally:

        if temp_file is not None:

            Path(
                temp_file.name
            ).unlink(
                missing_ok=True
            )

        await file.close()


# ==================================================
# MODEL
# ==================================================


@router.post("/model")
async def upload_model(

    file: UploadFile = File(...),

):

    if not file.filename:

        raise BadRequestError(

            "Upload file tidak memiliki nama."

        )

    if not file.filename.lower().endswith(

        ".zip"

    ):

        raise BadRequestError(

            "Model package harus berupa file ZIP."

        )

    temp_file = None

    total_size = 0

    try:

        # ------------------------------------------
        # Temporary ZIP
        # ------------------------------------------

        temp_file = NamedTemporaryFile(

            delete=False,

            suffix=".zip",

        )

        # ------------------------------------------
        # Stream upload
        # ------------------------------------------

        while True:

            chunk = await file.read(

                1024 * 1024

            )

            if not chunk:

                break

            total_size += len(chunk)

            if total_size > MODEL_MAX_SIZE:

                raise BadRequestError(

                    "Ukuran model package "
                    "melebihi batas 10 GB."

                )

            temp_file.write(chunk)

        temp_file.close()

        # ------------------------------------------
        # Install model
        # ------------------------------------------

        result = model_upload.upload_zip(

            Path(temp_file.name)

        )

        manifest = result["manifest"]

        # ------------------------------------------
        # Response
        # ------------------------------------------

        return success(

            message=(
                "Model uploaded successfully."
            ),

            data={

                "model": (
                    manifest.model_dump()
                ),

                "engine": {

                    "name": manifest.engine,

                    "registered": (
                        result[
                            "engine_registered"
                        ]
                    ),

                    "error": (
                        result[
                            "engine_error"
                        ]
                    ),

                },

            },

        )

    except FileExistsError as exc:

        raise HTTPException(

            status_code=409,

            detail=str(exc),

        )

    except zipfile.BadZipFile:

        raise BadRequestError(

            "File ZIP tidak valid atau rusak."

        )

    except ValueError as exc:

        raise BadRequestError(

            str(exc)

        )

    finally:

        if temp_file is not None:

            Path(
                temp_file.name
            ).unlink(
                missing_ok=True
            )

        await file.close()

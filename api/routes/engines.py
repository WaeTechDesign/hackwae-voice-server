"""
HackWae Voice Server

Engine Route
"""

from fastapi import APIRouter

from core.exceptions.errors import NotFoundError
from core.exceptions.errors import BadRequestError

from services.engine_service import engine_service


router = APIRouter()


# ==================================================
# LIST
# ==================================================

@router.get("/")
def list_engines():

    engines = engine_service.list()

    return {

        "success": True,

        "count": len(engines),

        "data": engines,

    }


# ==================================================
# GET
# ==================================================

@router.get("/{engine_name}")
def get_engine(
    engine_name: str,
):

    engine = engine_service.get(
        engine_name
    )

    if engine is None:

        raise NotFoundError(
            "Engine not found."
        )

    return {

        "success": True,

        "data": {

            "name": engine.name,

            "loaded": engine.loaded,

            "health": engine.health(),

            "model_path": str(
                engine.model_path
            ),

        },

    }


# ==================================================
# RELOAD SINGLE
# ==================================================

@router.post("/{engine_name}/reload")
def reload_engine(
    engine_name: str,
):

    try:

        engine = (
            engine_service.reload_engine(
                engine_name
            )
        )

    except RuntimeError as exc:

        raise BadRequestError(
            str(exc)
        )

    return {

        "success": True,

        "message": (
            f"Engine '{engine_name}' "
            "reloaded successfully."
        ),

        "data": {

            "name": engine.name,

            "loaded": engine.loaded,

        },

    }


# ==================================================
# UNLOAD
# ==================================================

@router.post("/{engine_name}/unload")
def unload_engine(
    engine_name: str,
):

    if not engine_service.exists(
        engine_name
    ):

        raise NotFoundError(
            "Engine not found."
        )

    if not engine_service.unload(
        engine_name
    ):

        raise BadRequestError(
            "Unable to unload engine."
        )

    return {

        "success": True,

        "message": (
            f"Engine '{engine_name}' "
            "unloaded successfully."
        ),

    }


# ==================================================
# RELOAD ALL
# ==================================================

@router.post("/reload")
def reload_all():

    engine_service.reload()

    return {

        "success": True,

        "message": (
            "All engines reloaded successfully."
        ),

        "data": engine_service.list(),

    }

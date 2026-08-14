"""
HackWae Voice Server

Model Route
"""

from fastapi import APIRouter

from core.engine_loader import engine_loader

from core.exceptions.errors import (
    BadRequestError,
    NotFoundError,
)

from core.responses.success import success

from schemas.manifest import ModelManifest

from services.model_service import model_service


router = APIRouter()


# ==================================================
# LIST
# ==================================================


@router.get("/")
def list_models():

    models = model_service.list()

    return success(

        data=[

            model.model_dump()

            for model in models

        ],

        count=len(models),

    )


# ==================================================
# DEFAULT
# ==================================================


@router.get("/default")
def default_model():

    model = model_service.default()

    if model is None:

        raise NotFoundError(

            "Default model not found."

        )

    return success(

        data=model.model_dump()

    )


# ==================================================
# GET
# ==================================================


@router.get("/{engine}")
def get_model(
    engine: str,
):

    model = model_service.get(

        engine

    )

    if model is None:

        raise NotFoundError(

            "Model not found."

        )

    return success(

        data=model.model_dump()

    )


# ==================================================
# UPDATE METADATA
# ==================================================


@router.put("/{engine}")
def update_model(

    engine: str,

    manifest: ModelManifest,

):

    engine = engine.lower()

    existing = model_service.get(

        engine

    )

    if existing is None:

        raise NotFoundError(

            "Model not found."

        )

    # ------------------------------------------
    # Engine cannot be changed through PUT
    # ------------------------------------------

    if manifest.engine.lower() != engine:

        raise BadRequestError(

            "Model engine cannot be changed."

        )

    # ------------------------------------------
    # Normalize
    # ------------------------------------------

    manifest.engine = engine

    try:

        updated = model_service.update(

            manifest

        )

    except Exception as exc:

        raise BadRequestError(

            str(exc)

        )

    # ------------------------------------------
    # Reload engine if registered
    # ------------------------------------------

    engine_reloaded = False

    engine_error = None

    try:

        if engine_loader.exists(
            engine
        ):

            engine_loader.reload_engine(

                engine

            )

            engine_reloaded = True

    except Exception as exc:

        engine_error = str(exc)

    return success(

        message=(

            "Model metadata updated "
            "successfully."

        ),

        data={

            "model": (

                updated.model_dump()

            ),

            "engine": {

                "reloaded": (
                    engine_reloaded
                ),

                "error": engine_error,

            },

        },

    )


# ==================================================
# DELETE
# ==================================================


@router.delete("/{engine}")
def delete_model(

    engine: str,

):

    engine = engine.lower()

    if not model_service.exists(

        engine

    ):

        raise NotFoundError(

            "Model not found."

        )

    # ------------------------------------------
    # Unregister engine first
    # ------------------------------------------

    engine_unregistered = False

    try:

        if engine_loader.exists(

            engine

        ):

            engine_loader.unregister(

                engine

            )

            engine_unregistered = True

    except Exception as exc:

        raise BadRequestError(

            f"Unable to unload engine: {exc}"

        )

    # ------------------------------------------
    # Remove model
    # ------------------------------------------

    try:

        removed = model_service.remove(

            engine

        )

    except Exception as exc:

        # --------------------------------------
        # Attempt to restore engine
        # --------------------------------------

        try:

            engine_loader.register(

                engine

            )

        except Exception:

            pass

        raise BadRequestError(

            str(exc)

        )

    if not removed:

        raise NotFoundError(

            "Model not found."

        )

    return success(

        message=(

            "Model deleted successfully."

        ),

        data={

            "engine": engine,

            "engine_unregistered": (

                engine_unregistered

            ),

        },

    )

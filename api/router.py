"""
HackWae Voice Server

API Router
"""

from fastapi import APIRouter

from api.routes.health import router as health_router
from api.routes.engines import router as engines_router
from api.routes.models import router as models_router
from api.routes.tts import router as tts_router
from api.routes.voices import router as voices_router
from api.routes.history import router as history_router
from api.routes.debug import router as debug_router
from api.routes.queue import router as queue_router
from api.routes.upload import router as upload_router

router = APIRouter()

router.include_router(
    health_router,
    tags=["Health"],
)

router.include_router(
    engines_router,
    prefix="/engines",
    tags=["Engines"],
)

router.include_router(
    models_router,
    prefix="/models",
    tags=["Models"],
)

router.include_router(
    voices_router,
    prefix="/voices",
    tags=["Voices"],
)

router.include_router(
    history_router,
    prefix="/history",
    tags=["History"],
)

router.include_router(
    tts_router,
    prefix="/tts",
    tags=["TTS"],
)

router.include_router(
    debug_router,
    prefix="/debug",
    tags=["Debug"],
)

router.include_router(
    queue_router,
    prefix="/queue",
    tags=["Queue"],
)

router.include_router(

    upload_router,

    prefix="/upload",

    tags=["Upload"],

)

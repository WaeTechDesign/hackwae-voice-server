"""
HackWae Voice Server

Health Route
"""

from fastapi import APIRouter

from core.engine_registry import engine_registry

router = APIRouter()


@router.get("/")
def health():

    return {
        "status": "ok",
        "service": "HackWae Voice Server",
        "version": "0.1.0",
        "engines": len(engine_registry.list()),
    }

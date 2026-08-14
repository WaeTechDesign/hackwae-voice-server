"""
HackWae Voice Server

Engine Service
"""

from services.engine.loader import loader
from services.engine.manager import manager
from services.engine.unloader import unloader


class EngineService:

    # --------------------------------------------------
    # Query
    # --------------------------------------------------

    list = manager.list

    get = manager.get

    exists = manager.exists

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    load = loader.load

    register = loader.register

    unregister = loader.unregister

    reload_engine = loader.reload_engine

    reload = loader.reload

    unload = unloader.unload


engine_service = EngineService()

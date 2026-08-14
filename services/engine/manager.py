"""
HackWae Voice Server

Engine Manager
"""

from core.engine_registry import engine_registry


class EngineManager:

    def list(self):

        return engine_registry.list()

    def get(
        self,
        name: str,
    ):

        return engine_registry.get(name)

    def exists(
        self,
        name: str,
    ):

        return engine_registry.exists(name)


manager = EngineManager()

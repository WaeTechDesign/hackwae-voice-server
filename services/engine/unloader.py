"""
HackWae Voice Server

Engine Unloader
"""

from core.engine_loader import engine_loader


class EngineUnloader:

    def unload(
        self,
        engine_name: str,
    ):

        return engine_loader.unregister(
            engine_name
        )


unloader = EngineUnloader()

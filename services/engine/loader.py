"""
HackWae Voice Server

Engine Loader Service
"""

from core.engine_loader import engine_loader


class EngineLoader:

    def load(self):

        return engine_loader.load()

    # --------------------------------------------------

    def register(
        self,
        engine_name: str,
    ):

        return engine_loader.register(
            engine_name
        )

    # --------------------------------------------------

    def unregister(
        self,
        engine_name: str,
    ):

        return engine_loader.unregister(
            engine_name
        )

    # --------------------------------------------------

    def reload_engine(
        self,
        engine_name: str,
    ):

        return engine_loader.reload_engine(
            engine_name
        )

    # --------------------------------------------------

    def reload(self):

        return engine_loader.reload()


loader = EngineLoader()

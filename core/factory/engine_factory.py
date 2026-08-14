"""
HackWae Voice Server

Engine Factory
"""

from engines.chatterbox.engine import ChatterboxEngine


class EngineFactory:

    def create(
        self,
        name: str,
    ):

        name = name.lower()

        if name == "chatterbox":
            return ChatterboxEngine()

        raise RuntimeError(
            f"Engine '{name}' belum didukung."
        )


engine_factory = EngineFactory()

"""
HackWae Voice Server

Engine Registry
"""

from interfaces.engine import EngineInterface


class EngineRegistry:

    def __init__(self):

        self._engines: dict[
            str,
            EngineInterface,
        ] = {}

    # --------------------------------------------------

    def register(
        self,
        engine: EngineInterface,
    ) -> None:

        self._engines[engine.name] = engine

    # --------------------------------------------------

    def unregister(
        self,
        name: str,
    ) -> EngineInterface | None:

        return self._engines.pop(
            name,
            None,
        )

    # --------------------------------------------------

    def replace(
        self,
        engine: EngineInterface,
    ) -> EngineInterface | None:

        previous = self.unregister(
            engine.name
        )

        self.register(engine)

        return previous

    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> EngineInterface | None:

        return self._engines.get(name)

    # --------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._engines

    # --------------------------------------------------

    def list(self) -> list[str]:

        return sorted(
            self._engines.keys()
        )

    # --------------------------------------------------

    def count(self) -> int:

        return len(
            self._engines
        )

    # --------------------------------------------------

    def clear(self) -> None:

        self._engines.clear()


engine_registry = EngineRegistry()

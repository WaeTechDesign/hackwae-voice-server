"""
HackWae Voice Server

Engine Loader
"""

from core.engine_registry import engine_registry
from core.factory.engine_factory import engine_factory

from services.model_manager import model_manager

from utils.logger import logger


class EngineLoader:

    # ==================================================
    # INITIAL / SAFE LOAD
    # ==================================================

    def load(self) -> None:

        logger.info(
            "Loading enabled engines..."
        )

        manifests = model_manager.scan()

        for manifest in manifests:

            engine_name = manifest.engine

            # ------------------------------------------
            # Already registered
            # ------------------------------------------

            if engine_registry.exists(
                engine_name
            ):

                logger.info(
                    f"Engine already registered: "
                    f"{engine_name}"
                )

                continue

            # ------------------------------------------
            # Register
            # ------------------------------------------

            try:

                self._register_manifest(
                    manifest
                )

            except Exception as exc:

                logger.error(
                    f"Failed to register engine "
                    f"'{engine_name}': {exc}"
                )

                logger.exception(exc)

                # --------------------------------------
                # IMPORTANT:
                # Jangan hentikan engine lain.
                # --------------------------------------

                continue

        logger.info(
            f"Registered "
            f"{engine_registry.count()} "
            f"engine(s)."
        )

    # ==================================================
    # REGISTER SINGLE ENGINE
    # ==================================================

    def register(
        self,
        engine_name: str,
    ):

        engine_name = engine_name.lower()

        manifest = model_manager.get(
            engine_name
        )

        if manifest is None:

            raise RuntimeError(
                f"Model manifest not found: "
                f"{engine_name}"
            )

        return self._register_manifest(
            manifest
        )

    # ==================================================
    # EXISTS
    # ==================================================

    def exists(
        self,
        engine_name: str,
    ) -> bool:

        return engine_registry.exists(
            engine_name.lower()
        )

    # ==================================================
    # INTERNAL REGISTER
    # ==================================================

    def _register_manifest(
        self,
        manifest,
    ):

        engine_name = manifest.engine.lower()

        logger.info(
            f"Registering {engine_name}"
        )

        engine = engine_factory.create(
            engine_name
        )

        engine_registry.register(
            engine
        )

        logger.success(
            f"Engine registered: "
            f"{engine_name}"
        )

        return engine

    # ==================================================
    # UNREGISTER
    # ==================================================

    def unregister(
        self,
        engine_name: str,
    ) -> bool:

        engine_name = engine_name.lower()

        engine = engine_registry.get(
            engine_name
        )

        if engine is None:

            logger.warning(
                f"Engine not registered: "
                f"{engine_name}"
            )

            return False

        # ------------------------------------------

        try:

            if engine.loaded:

                logger.info(
                    f"Unloading engine: "
                    f"{engine_name}"
                )

                engine.unload()

        except Exception as exc:

            logger.error(
                f"Failed to unload engine "
                f"'{engine_name}': {exc}"
            )

            logger.exception(exc)

            raise

        # ------------------------------------------

        engine_registry.unregister(
            engine_name
        )

        logger.success(
            f"Engine unregistered: "
            f"{engine_name}"
        )

        return True

    # ==================================================
    # RELOAD SINGLE ENGINE
    # ==================================================

    def reload_engine(
        self,
        engine_name: str,
    ):

        engine_name = engine_name.lower()

        logger.info(
            f"Reloading engine: "
            f"{engine_name}"
        )

        if engine_registry.exists(
            engine_name
        ):

            self.unregister(
                engine_name
            )

        return self.register(
            engine_name
        )

    # ==================================================
    # RELOAD ALL
    # ==================================================

    def reload(self) -> None:

        logger.info(
            "Reloading all engines..."
        )

        existing = engine_registry.list()

        for engine_name in existing:

            try:

                self.unregister(
                    engine_name
                )

            except Exception as exc:

                logger.error(
                    f"Failed to unload "
                    f"'{engine_name}': {exc}"
                )

        self.load()

        logger.success(
            f"Engine reload complete. "
            f"{engine_registry.count()} "
            f"engine(s) registered."
        )


engine_loader = EngineLoader()

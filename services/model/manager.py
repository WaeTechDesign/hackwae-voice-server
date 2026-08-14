"""
HackWae Voice Server

Model Manager
"""

from pathlib import Path

from core.config import settings

from schemas.manifest import ModelManifest

from .scanner import scanner
from .creator import creator
from .updater import updater
from .remover import remover


class ModelManager:

    # ==================================================
    # LIST
    # ==================================================

    def scan(
        self,
    ) -> list[ModelManifest]:

        return scanner.scan()

    # ==================================================
    # GET
    # ==================================================

    def get(
        self,
        engine: str,
    ) -> ModelManifest | None:

        engine = engine.lower()

        for model in self.scan():

            if model.engine.lower() == engine:

                return model

        return None

    # ==================================================
    # EXISTS
    # ==================================================

    def exists(
        self,
        engine: str,
    ) -> bool:

        return self.get(engine) is not None

    # ==================================================
    # DEFAULT
    # ==================================================

    def default(
        self,
    ) -> ModelManifest | None:

        for model in self.scan():

            if model.default:

                return model

        return None

    # ==================================================
    # CREATE
    # ==================================================

    def create(
        self,
        manifest: ModelManifest,
        source: Path,
    ) -> ModelManifest:

        manifest.engine = (
            manifest.engine.lower()
        )

        return creator.create(

            manifest,

            source,

        )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        manifest: ModelManifest,
    ) -> ModelManifest:

        manifest.engine = (
            manifest.engine.lower()
        )

        directory = (

            settings.paths.models

            / manifest.engine

        )

        return updater.update(

            directory,

            manifest,

        )

    # ==================================================
    # REMOVE
    # ==================================================

    def remove(
        self,
        engine: str,
    ) -> bool:

        return remover.remove(

            engine.lower()

        )


manager = ModelManager()

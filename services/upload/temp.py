"""
HackWae Voice Server

Temporary Upload
"""

import shutil
from pathlib import Path
from uuid import uuid4

from core.config import settings


class TemporaryStorage:

    def create(self) -> Path:

        directory = (

            settings.paths.storage

            / "temp"

            / uuid4().hex

        )

        directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        return directory

    # --------------------------------------------------

    def remove(

        self,

        directory: Path,

    ):

        if directory.exists():

            shutil.rmtree(directory)


temporary = TemporaryStorage()

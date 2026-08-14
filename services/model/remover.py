"""
HackWae Voice Server

Model Remover
"""

import shutil

from core.config import settings


class ModelRemover:

    # --------------------------------------------------

    def remove(

        self,

        engine: str,

    ) -> bool:

        directory = (

            settings.paths.models

            / engine

        )

        if not directory.exists():

            return False

        shutil.rmtree(directory)

        return True


remover = ModelRemover()

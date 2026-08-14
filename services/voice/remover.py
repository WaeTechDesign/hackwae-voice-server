"""
HackWae Voice Server

Voice Remover
"""

import shutil
from pathlib import Path


class VoiceRemover:

    # --------------------------------------------------

    def remove(

        self,

        directory: Path,

    ) -> bool:

        if not directory.exists():

            return False

        shutil.rmtree(directory)

        return True


remover = VoiceRemover()

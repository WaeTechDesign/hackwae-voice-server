"""
HackWae Voice Server

Voice Database
"""

import json
from pathlib import Path


class VoiceDatabase:

    def load(
        self,
        path: Path,
    ):

        if not path.exists():

            return None

        with open(

            path,

            "r",

            encoding="utf-8",

        ) as file:

            return json.load(file)

    # ------------------------------------------

    def save(

        self,

        path: Path,

        data,

    ):

        with open(

            path,

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False,

            )


database = VoiceDatabase()

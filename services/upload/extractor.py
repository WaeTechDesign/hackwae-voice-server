"""
HackWae Voice Server

ZIP Extractor
"""

import zipfile
from pathlib import Path


class Extractor:

    # --------------------------------------------------

    def extract(

        self,

        archive: Path,

        output: Path,

    ):

        with zipfile.ZipFile(archive, "r") as zip_file:

            for member in zip_file.infolist():

                target = (

                    output

                    / member.filename

                ).resolve()

                root = output.resolve()

                if not str(target).startswith(

                    str(root) + "/"

                ):

                    raise ValueError(

                        "Invalid ZIP archive: "
                        "path traversal detected."

                    )

            zip_file.extractall(output)


extractor = Extractor()

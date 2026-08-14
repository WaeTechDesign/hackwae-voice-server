"""
HackWae Voice Server

History Cleaner
"""

from __future__ import annotations

from .database import database
from .manager import manager


class HistoryCleaner:

    # --------------------------------------------------

    def delete(
        self,
        filename: str,
    ) -> bool:

        filename = manager._validate_filename(
            filename
        )

        file = (
            database.directory
            / filename
        )

        data = database.load()

        matching = [
            item
            for item in data
            if item.get("filename")
            == filename
        ]

        if not matching and not file.is_file():
            return False

        # ------------------------------------------
        # Hapus file terlebih dahulu.
        # ------------------------------------------

        if file.is_file():
            file.unlink()

        # ------------------------------------------
        # Hapus metadata yang terkait dengan file.
        # ------------------------------------------

        new_data = [
            item
            for item in data
            if item.get("filename")
            != filename
        ]

        if len(new_data) != len(data):
            database.save(new_data)

        return True

    # --------------------------------------------------

    def clear(self) -> int:

        data = database.load()

        deleted_files = 0

        filenames = {
            item.get("filename")
            for item in data
            if item.get("filename")
        }

        # ------------------------------------------
        # Hapus seluruh file yang tercatat.
        # ------------------------------------------

        for filename in filenames:

            try:

                filename = (
                    manager._validate_filename(
                        filename
                    )
                )

            except ValueError:
                continue

            file = (
                database.directory
                / filename
            )

            if file.is_file():

                file.unlink()

                deleted_files += 1

        # ------------------------------------------
        # Bersihkan metadata.
        # ------------------------------------------

        database.save([])

        return deleted_files


cleaner = HistoryCleaner()

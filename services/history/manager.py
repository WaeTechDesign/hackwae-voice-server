"""
HackWae Voice Server

History Manager
"""

from __future__ import annotations

from pathlib import Path

from schemas.history import HistoryItem

from .database import database


class HistoryManager:

    # --------------------------------------------------
    # LIST
    # --------------------------------------------------

    def list(self) -> list[dict]:

        return database.load()

    # --------------------------------------------------
    # ADD / UPSERT
    # --------------------------------------------------

    def add(
        self,
        item: HistoryItem,
    ) -> HistoryItem:

        filename = self._validate_filename(
            item.filename
        )

        file = database.directory / filename

        if not file.is_file():
            raise FileNotFoundError(
                f"History audio file tidak ditemukan: "
                f"{filename}"
            )

        data = database.load()

        new_item = item.model_dump(
            mode="json"
        )

        # ------------------------------------------
        # Filename adalah unique key.
        #
        # Jika filename sudah ada, metadata lama
        # diganti dengan metadata terbaru.
        # ------------------------------------------

        replaced = False

        new_data = []

        for existing in data:

            if existing.get("filename") == filename:

                if not replaced:

                    new_data.append(
                        new_item
                    )

                    replaced = True

                # Skip duplicate record lainnya.

                continue

            new_data.append(existing)

        # ------------------------------------------
        # Jika filename belum ada, tambahkan baru.
        # ------------------------------------------

        if not replaced:

            new_data.append(new_item)

        database.save(new_data)

        return item

    # --------------------------------------------------
    # GET FILE
    # --------------------------------------------------

    def get(
        self,
        filename: str,
    ) -> Path | None:

        filename = self._validate_filename(
            filename
        )

        file = database.directory / filename

        if not file.is_file():
            return None

        for item in database.load():

            if item.get("filename") == filename:

                return file

        return None

    # --------------------------------------------------
    # EXISTS
    # --------------------------------------------------

    def exists(
        self,
        filename: str,
    ) -> bool:

        filename = self._validate_filename(
            filename
        )

        return (
            database.directory / filename
        ).is_file()

    # --------------------------------------------------
    # METADATA
    # --------------------------------------------------

    def metadata(
        self,
        filename: str,
    ) -> dict | None:

        filename = self._validate_filename(
            filename
        )

        for item in database.load():

            if item.get("filename") == filename:

                return item

        return None

    # --------------------------------------------------
    # REMOVE METADATA
    # --------------------------------------------------

    def remove_metadata(
        self,
        filename: str,
        item_id: str | None = None,
    ) -> bool:

        filename = self._validate_filename(
            filename
        )

        data = database.load()

        if item_id is None:

            new_data = [
                item
                for item in data
                if item.get("filename")
                != filename
            ]

        else:

            new_data = [
                item
                for item in data
                if not (
                    item.get("filename")
                    == filename
                    and item.get("id")
                    == item_id
                )
            ]

        if len(new_data) == len(data):

            return False

        database.save(new_data)

        return True

    # --------------------------------------------------
    # VALIDATE FILENAME
    # --------------------------------------------------

    def _validate_filename(
        self,
        filename: str,
    ) -> str:

        if not filename:

            raise ValueError(
                "Filename tidak boleh kosong."
            )

        path = Path(filename)

        if (
            path.name != filename
            or path.is_absolute()
            or filename in (".", "..")
            or "/" in filename
            or "\\" in filename
            or ".." in filename
        ):

            raise ValueError(
                "Filename tidak valid."
            )

        if len(filename) > 255:

            raise ValueError(
                "Filename terlalu panjang."
            )

        return filename


manager = HistoryManager()

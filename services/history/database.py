"""
HackWae Voice Server

History Database
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from core.config import settings


class HistoryDatabase:

    def __init__(self):
        self.directory = settings.paths.history
        self.file = self.directory / "history.json"

        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file.exists():
            self._atomic_write([])

    # --------------------------------------------------

    def load(self) -> list[dict]:

        try:
            raw = self.file.read_text(
                encoding="utf-8",
            )

            data = json.loads(raw)

        except (
            json.JSONDecodeError,
            OSError,
        ) as exc:

            raise RuntimeError(
                "History database tidak dapat dibaca."
            ) from exc

        if not isinstance(data, list):
            raise RuntimeError(
                "Format history database tidak valid."
            )

        return data

    # --------------------------------------------------

    def save(
        self,
        data: list[dict],
    ) -> None:

        if not isinstance(data, list):
            raise ValueError(
                "History database harus berupa list."
            )

        self._atomic_write(data)

    # --------------------------------------------------

    def _atomic_write(
        self,
        data: list[dict],
    ) -> None:

        payload = json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
        )

        temp_path: Path | None = None

        try:

            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.directory,
                prefix=".history-",
                suffix=".tmp",
                delete=False,
            ) as temp:

                temp.write(payload)
                temp.flush()
                os.fsync(temp.fileno())

                temp_path = Path(
                    temp.name
                )

            os.replace(
                temp_path,
                self.file,
            )

        except OSError as exc:

            if temp_path is not None:
                temp_path.unlink(
                    missing_ok=True
                )

            raise RuntimeError(
                "Gagal menyimpan history database."
            ) from exc


database = HistoryDatabase()

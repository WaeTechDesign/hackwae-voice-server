"""
HackWae Voice Server

Queue Database
"""

import json

from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from services.queue.job import QueueJob


class QueueDatabase:

    def __init__(self):

        self.file = Path(
            "storage/queue/queue.json"
        )

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file.exists():

            self.file.write_text(
                "[]",
                encoding="utf-8",
            )

    # ==================================================
    # LOAD
    # ==================================================

    def load(self) -> list[QueueJob]:

        raw = json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )

        jobs = []

        for item in raw:

            # ------------------------------------------
            # Backward compatibility
            # ------------------------------------------
            #
            # Queue lama tidak memiliki
            # requested_output.
            #
            # Jika job lama sudah memiliki output,
            # kita tidak menganggap output tersebut
            # sebagai requested_output.
            #
            # Dengan begitu retry job lama akan
            # menggunakan filename otomatis baru.
            # ------------------------------------------

            requested_output = item.get(
                "requested_output"
            )

            output = (
                Path(item["output"])
                if item.get("output")
                else None
            )

            # ------------------------------------------
            # Datetime
            # ------------------------------------------

            created = datetime.fromisoformat(
                item["created"]
            )

            started = (
                datetime.fromisoformat(
                    item["started"]
                )
                if item.get("started")
                else None
            )

            finished = (
                datetime.fromisoformat(
                    item["finished"]
                )
                if item.get("finished")
                else None
            )

            # ------------------------------------------
            # Queue Job
            # ------------------------------------------

            jobs.append(
                QueueJob(
                    id=item["id"],
                    text=item.get(
                        "text",
                        "",
                    ),
                    voice=item.get(
                        "voice",
                        "putri",
                    ),
                    engine=item.get(
                        "engine",
                        "chatterbox",
                    ),
                    requested_output=requested_output,
                    output=output,
                    status=item.get(
                        "status",
                        "queued",
                    ),
                    progress=item.get(
                        "progress",
                        0,
                    ),
                    created=created,
                    started=started,
                    finished=finished,
                    error=item.get(
                        "error"
                    ),
                )
            )

        return jobs

    # ==================================================
    # SAVE
    # ==================================================

    def save(
        self,
        jobs: list[QueueJob],
    ):

        data = []

        for job in jobs:

            item = asdict(job)

            # ------------------------------------------
            # Datetime
            # ------------------------------------------

            item["created"] = (
                item["created"].isoformat()
            )

            item["started"] = (
                item["started"].isoformat()
                if item["started"]
                else None
            )

            item["finished"] = (
                item["finished"].isoformat()
                if item["finished"]
                else None
            )

            # ------------------------------------------
            # Path
            # ------------------------------------------

            item["output"] = (
                str(item["output"])
                if item["output"]
                else None
            )

            # ------------------------------------------
            # requested_output sudah string / None
            # ------------------------------------------

            data.append(item)

        self.file.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )


database = QueueDatabase()

"""
HackWae Voice Server

Queue Manager
"""

from collections import deque

from .database.database import database
from .job import QueueJob


class QueueManager:

    def __init__(self):

        self.jobs = {}

        self.queue = deque()

        self.load()

    # ==================================================
    # LOAD
    # ==================================================

    def load(self):

        self.jobs.clear()

        self.queue.clear()

        jobs = database.load()

        for job in jobs:

            self.jobs[job.id] = job

    # ==================================================
    # SAVE
    # ==================================================

    def save(self):

        database.save(
            list(
                self.jobs.values()
            )
        )

    # ==================================================
    # CREATE
    # ==================================================

    def create(
        self,
        text,
        voice,
        engine,
        output=None,
    ):

        job = QueueJob(
            text=text,
            voice=voice,
            engine=engine,
            requested_output=output,
            output=None,
        )

        self.jobs[job.id] = job

        self.queue.append(
            job.id
        )

        self.save()

        return job

    # ==================================================
    # GET
    # ==================================================

    def get(
        self,
        job_id,
    ):

        return self.jobs.get(
            job_id
        )

    # ==================================================
    # NEXT
    # ==================================================

    def next(self):

        while self.queue:

            job_id = self.queue.popleft()

            job = self.jobs.get(job_id)

            # Job sudah tidak ada.
            if job is None:
                continue

            # Hanya job QUEUED yang boleh diberikan
            # kepada worker.
            if job.status != "queued":

                continue

            self.save()

            return job

        return None

    # ==================================================
    # LIST
    # ==================================================

    def list(self):

        return list(
            self.jobs.values()
        )

    # ==================================================
    # REMOVE
    # ==================================================

    def remove(
        self,
        job_id,
    ):

        if job_id not in self.jobs:

            return False

        self.jobs.pop(
            job_id
        )

        # ----------------------------------------------
        # Remove pending occurrences from queue
        # ----------------------------------------------

        self.queue = deque(
            item
            for item in self.queue
            if item != job_id
        )

        self.save()

        return True

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self):

        self.jobs.clear()

        self.queue.clear()

        self.save()


queue_manager = QueueManager()

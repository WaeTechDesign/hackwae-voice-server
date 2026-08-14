"""
HackWae Voice Server

Queue Actions
"""

from utils.logger import logger

from .manager import queue_manager
from .status import QueueStatus


class QueueActions:

    # --------------------------------------------------
    # Retry
    # --------------------------------------------------

    def retry(
        self,
        job_id: str,
    ):

        job = queue_manager.get(job_id)

        if job is None:
            return False

        # Retry hanya boleh untuk
        # job yang berstatus failed.
        if job.status != QueueStatus.FAILED:
            return False

        job.status = QueueStatus.QUEUED

        job.progress = 0

        job.error = None

        job.started = None

        job.finished = None

        queue_manager.queue.append(job.id)

        queue_manager.save()

        logger.info(
            f"[Queue] Retry : {job.id}"
        )

        return True

    # --------------------------------------------------
    # Cancel
    # --------------------------------------------------

    def cancel(
        self,
        job_id: str,
    ):

        job = queue_manager.get(job_id)

        if job is None:
            return False

        # Cancel hanya boleh untuk
        # job yang masih berada di queue.
        if job.status != QueueStatus.QUEUED:
            return False

        job.status = "cancelled"

        job.progress = 0

        job.error = None

        job.started = None

        job.finished = None

        queue_manager.save()

        logger.info(
            f"[Queue] Cancel : {job.id}"
        )

        return True


queue_actions = QueueActions()

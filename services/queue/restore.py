"""
HackWae Voice Server

Queue Restore
"""

from utils.logger import logger

from .manager import queue_manager
from .status import QueueStatus


class QueueRestore:

    # --------------------------------------------------

    def restore(self):

        logger.info(
            "[Queue] Restoring Queue..."
        )

        queue_manager.load()

        restored = 0

        for job in queue_manager.list():

            if job.status in (

                QueueStatus.QUEUED,

                QueueStatus.RUNNING,

            ):

                job.status = QueueStatus.QUEUED

                job.progress = 0

                queue_manager.queue.append(job.id)

                restored += 1

        logger.success(

            f"[Queue] Restored {restored} job(s)."

        )

        queue_manager.save()


queue_restore = QueueRestore()

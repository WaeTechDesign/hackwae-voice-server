"""
HackWae Voice Server

Queue Statistics
"""

from .manager import queue_manager
from .status import QueueStatus


class QueueStatistics:

    def summary(self):

        jobs = queue_manager.list()

        return {

            "total": len(jobs),

            "queued": sum(
                job.status == QueueStatus.QUEUED
                for job in jobs
            ),

            "running": sum(
                job.status == QueueStatus.RUNNING
                for job in jobs
            ),

            "finished": sum(
                job.status == QueueStatus.FINISHED
                for job in jobs
            ),

            "failed": sum(
                job.status == QueueStatus.FAILED
                for job in jobs
            ),

            "cancelled": sum(
                job.status == "cancelled"
                for job in jobs
            ),

        }


queue_statistics = QueueStatistics()

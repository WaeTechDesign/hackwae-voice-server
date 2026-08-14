"""
HackWae Voice Server

Queue Worker
"""

from datetime import datetime
import threading
import time

from services.tts_service import tts_service

from utils.logger import logger

from .manager import queue_manager
from .restore import queue_restore
from .status import QueueStatus


class QueueWorker:

    def __init__(self):

        self.running = False

    # ==================================================
    # PROCESS
    # ==================================================

    def process(self, job):

        logger.info(
            f"[Worker] Job Received : {job.id}"
        )

        # --------------------------------------------------
        # Cancellation guard
        # --------------------------------------------------
        #
        # Job mungkin sudah dibatalkan setelah ID diambil
        # dari queue tetapi sebelum process() dijalankan.
        #
        # Jangan pernah memproses job yang bukan QUEUED.
        # --------------------------------------------------

        if job.status != QueueStatus.QUEUED:

            logger.info(
                f"[Worker] Skip job {job.id} "
                f"(status: {job.status})"
            )

            return

        logger.info(
            f"[Worker] Engine : {job.engine}"
        )

        logger.info(
            f"[Worker] Voice : {job.voice}"
        )

        logger.info(
            f"[Worker] Requested Output : "
            f"{job.requested_output}"
        )

        # ----------------------------------------------
        # Running state
        # ----------------------------------------------

        job.status = QueueStatus.RUNNING

        job.started = datetime.utcnow()

        job.finished = None

        job.error = None

        job.progress = 0

        queue_manager.save()

        logger.info(
            f"[Worker] Processing : {job.id}"
        )

        try:

            # ------------------------------------------
            # Generate TTS
            #
            # IMPORTANT:
            # requested_output = user request
            # output           = actual result
            # ------------------------------------------

            result = tts_service.generate(

                text=job.text,

                voice=job.voice,

                engine=job.engine,

                output=job.requested_output,

            )

            # ------------------------------------------
            # Actual generated file
            # ------------------------------------------

            result_path = result["path"]

            # ------------------------------------------
            # Cancellation guard after generation
            # ------------------------------------------
            #
            # Jangan mengubah job menjadi FINISHED kalau
            # state sudah berubah menjadi CANCELLED.
            #
            # Ini juga melindungi state machine dari perubahan
            # state yang terjadi selama proses generate.
            # ------------------------------------------

            if job.status == "cancelled":

                logger.warning(
                    f"[Worker] Job cancelled after generation : "
                    f"{job.id}"
                )

                return

            # Queue stores filename only.
            job.output = result_path.name

            # ------------------------------------------
            # Finished
            # ------------------------------------------

            job.progress = 100

            job.status = QueueStatus.FINISHED

            job.error = None

            queue_manager.save()

            logger.success(
                f"[Worker] Finished : {job.id}"
            )

            logger.info(
                f"[Worker] Output : {result_path}"
            )

        except Exception as e:

            # ------------------------------------------
            # Failed
            # ------------------------------------------

            # Jangan mengubah cancelled menjadi failed.
            if job.status == "cancelled":

                logger.warning(
                    f"[Worker] Job cancelled : {job.id}"
                )

                return

            job.status = QueueStatus.FAILED

            job.error = str(e)

            queue_manager.save()

            logger.error(
                f"[Worker] Failed : {job.id}"
            )

            logger.exception(e)

        finally:

            # Hanya isi finished timestamp untuk job
            # yang benar-benar sudah diproses.
            if job.status in (
                QueueStatus.FINISHED,
                QueueStatus.FAILED,
            ):

                job.finished = datetime.utcnow()

                queue_manager.save()

    # ==================================================
    # LOOP
    # ==================================================

    def loop(self):

        logger.info(
            "[Worker] Queue Worker Loop Running"
        )

        while self.running:

            job = queue_manager.next()

            if job is None:

                time.sleep(0.25)

                continue

            self.process(job)

    # ==================================================
    # START
    # ==================================================

    def start(self):

        if self.running:

            logger.warning(
                "[Worker] Already Running"
            )

            return

        self.running = True

        queue_restore.restore()

        logger.info(
            "[Worker] Queue Worker Started"
        )

        threading.Thread(

            target=self.loop,

            daemon=True,

            name="QueueWorker",

        ).start()

    # ==================================================
    # STOP
    # ==================================================

    def stop(self):

        self.running = False

        logger.info(
            "[Worker] Queue Worker Stopped"
        )


worker = QueueWorker()

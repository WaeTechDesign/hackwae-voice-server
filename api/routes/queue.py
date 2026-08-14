"""
HackWae Voice Server

Queue Route
"""

from fastapi import APIRouter

from core.exceptions.errors import (
    BadRequestError,
    NotFoundError,
)

from core.responses.success import success

from services.queue.actions import queue_actions
from services.queue.manager import queue_manager
from services.queue.statistics import queue_statistics

router = APIRouter()


# --------------------------------------------------

@router.get("/")
def list_queue():

    return success(

        data=[

            {

                "id": job.id,

                "status": job.status,

                "progress": job.progress,

                "voice": job.voice,

                "engine": job.engine,

                "created": job.created,

            }

            for job in queue_manager.list()

        ],

    )


# --------------------------------------------------

@router.get("/stats")
def stats():

    return success(

        data=queue_statistics.summary(),

    )


# --------------------------------------------------

@router.get("/{job_id}")
def get_job(job_id: str):

    job = queue_manager.get(job_id)

    if job is None:

        raise NotFoundError(

            "Queue job not found."

        )

    return success(

        data={

            "id": job.id,

            "text": job.text,

            "voice": job.voice,

            "engine": job.engine,

            "status": job.status,

            "progress": job.progress,

            "created": job.created,

            "started": job.started,

            "finished": job.finished,

            "error": job.error,

            "output": (

                str(job.output)

                if job.output

                else None

            ),

        },

    )


# --------------------------------------------------

@router.delete("/{job_id}")
def delete_job(job_id: str):

    if not queue_manager.remove(job_id):

        raise NotFoundError(

            "Queue job not found."

        )

    return success(

        message="Queue job deleted successfully.",

    )


# --------------------------------------------------

@router.delete("/")
def clear_queue():

    queue_manager.clear()

    return success(

        message="Queue cleared.",

    )


# --------------------------------------------------

@router.post("/{job_id}/retry")
def retry(job_id: str):

    if not queue_actions.retry(job_id):

        raise BadRequestError(

            "Unable to retry queue job."

        )

    return success(

        message="Queue job requeued.",

    )


# --------------------------------------------------

@router.post("/{job_id}/cancel")
def cancel(job_id: str):

    if not queue_actions.cancel(job_id):

        raise BadRequestError(

            "Unable to cancel queue job."

        )

    return success(

        message="Queue job cancelled.",

    )

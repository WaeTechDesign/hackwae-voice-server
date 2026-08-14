"""
HackWae Voice Server

Debug Route
"""

from fastapi import APIRouter

from services.queue.manager import queue_manager

router = APIRouter()


@router.post("/queue-test")
def queue_test():

    job = queue_manager.create(

        text="Halo dari Queue Worker",

        voice="putri",

        engine="chatterbox",

    )

    return {

        "success": True,

        "job_id": job.id,

        "status": job.status,

    }

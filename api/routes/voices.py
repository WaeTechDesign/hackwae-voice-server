"""
HackWae Voice Server

Voice Route
"""

from fastapi import APIRouter

from core.exceptions.errors import NotFoundError
from core.responses.success import success

from services.voice_service import voice_service

router = APIRouter()


# --------------------------------------------------

@router.get("/")
def list_voices():

    voices = voice_service.list()

    return success(

        data=[

            voice.model_dump()

            for voice in voices

        ],

        count=len(voices),

    )


# --------------------------------------------------

@router.get("/{voice_id}")
def get_voice(voice_id: str):

    voice = voice_service.get(voice_id)

    if voice is None:

        raise NotFoundError(

            "Voice not found."

        )

    return success(

        data=voice.model_dump(),

    )


# --------------------------------------------------

@router.delete("/{voice_id}")
def delete_voice(voice_id: str):

    if not voice_service.remove(voice_id):

        raise NotFoundError(

            "Voice not found."

        )

    return success(

        message="Voice deleted successfully.",

    )

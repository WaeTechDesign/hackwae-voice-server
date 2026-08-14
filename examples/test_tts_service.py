from pathlib import Path

from core.engine_registry import engine_registry

from engines.chatterbox.engine import ChatterboxEngine

from services.tts_service import tts_service


engine_registry.register(
    ChatterboxEngine()
)

output = tts_service.generate(

    engine="chatterbox",

    voice="putri",

    text="Halo, saya adalah HackWae Voice Server.",

    output=Path("/tmp/hackwae_service.wav"),

)

print()

print(output)

print()

print("OK")

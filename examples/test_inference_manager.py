from pathlib import Path

from core.engine_registry import engine_registry
from examples.dummy_engine import DummyEngine
from services.inference_manager import inference_manager

dummy = DummyEngine(
    name="dummy",
    model_path=Path("/tmp"),
)

engine_registry.register(dummy)

result = inference_manager.tts(
    engine="dummy",
    voice="putri",
    text="Halo dari HackWae Voice Server",
)

print()

print(result)

print()

print("OK")

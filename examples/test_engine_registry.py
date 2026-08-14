from pathlib import Path

from core.engine_registry import engine_registry
from examples.dummy_engine import DummyEngine

dummy = DummyEngine(
    name="dummy",
    model_path=Path("/tmp")
)

engine_registry.register(dummy)

print()

print(engine_registry.list())

print()

print(engine_registry.exists("dummy"))

print()

engine = engine_registry.get("dummy")

print(engine.name)

print(engine.generate())

print()

engine_registry.unregister("dummy")

print(engine_registry.list())

print()

print("OK")

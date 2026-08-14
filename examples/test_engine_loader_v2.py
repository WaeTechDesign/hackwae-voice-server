from core.engine_loader import engine_loader
from core.engine_registry import engine_registry

engine_loader.load()

print()

print(engine_registry.list())

print()

print("OK")

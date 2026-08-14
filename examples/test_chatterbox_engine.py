from engines.chatterbox.engine import ChatterboxEngine

engine = ChatterboxEngine()

print()

print(engine.name)

print(engine.loaded)

engine.load()

print(engine.loaded)

print()

print(engine.health())

print()

print("OK")

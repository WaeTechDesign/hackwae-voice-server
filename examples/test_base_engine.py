from pathlib import Path

from core.base_engine import BaseEngine


class DummyEngine(BaseEngine):
    def generate(self, *args, **kwargs):
        return "Hello"


def main():
    engine = DummyEngine(
        name="dummy",
        model_path=Path("/tmp"),
    )

    print(engine.name)
    print(engine.loaded)

    engine.load()

    print(engine.loaded)
    print(engine.health())

    engine.unload()

    print(engine.loaded)
    print(engine.generate())

    print("OK")


if __name__ == "__main__":
    main()

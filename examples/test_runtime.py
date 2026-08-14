from pathlib import Path

from engines.chatterbox.runtime import runtime

result = runtime.generate(
    model_dir=Path("/ai/models/chatterbox"),
    text="Halo semuanya, ini adalah HackWae Voice Server.",
    voice=Path("/ai/voices/female/putri/voice.wav"),
    output=Path("/tmp/runtime_test.wav"),
)

print()

print(result)

print()

print("OK")

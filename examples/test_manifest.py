from pathlib import Path

from providers.manifest import manifest_provider

manifest = manifest_provider.load(
    Path("/ai/models/chatterbox/manifest.yaml")
)

print()

print(manifest)

print()

print(manifest.name)

print(manifest.engine)

print(manifest.language)

print(manifest.voice_clone)

print("OK")

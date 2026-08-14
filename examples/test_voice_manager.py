from services.voice_manager import voice_manager

voices = voice_manager.scan()

print()

print("Voices Found :", len(voices))

print()

for voice in voices:

    print("------------------------")

    print(voice.name)

    print(voice.gender)

    print(voice.language)

    print(voice.engines)

    print(voice.default)

print()

default = voice_manager.default()

print("Default Voice")

print(default.name)

print()

print("Exists :", voice_manager.exists("putri"))

print()

print("OK")

from services.model_manager import model_manager

print("Models Root :", model_manager.models_root)

print("Engines :")

for engine in model_manager.scan():
    print("-", engine)

print()

print("Chatterbox :", model_manager.exists("chatterbox"))
print("FishSpeech:", model_manager.exists("fish-speech"))
print("Whisper   :", model_manager.exists("whisper"))

print()

print("OK")

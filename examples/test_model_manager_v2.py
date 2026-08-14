from services.model_manager import model_manager

models = model_manager.scan()

print()

print(f"Found {len(models)} model(s)\n")

for model in models:

    print("----------------------------")

    print(model.name)

    print(model.engine)

    print(model.language)

    print(model.voice_clone)

    print(model.default)

print()

print("OK")

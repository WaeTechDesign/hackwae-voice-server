from services.model_manager import model_manager

model = model_manager.default_model()

print()

print(model.name)

print(model.engine)

print(model.language)

print()

print("OK")

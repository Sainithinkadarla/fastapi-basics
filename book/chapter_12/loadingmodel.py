import os
import joblib

model_dir = os.path.dirname(__file__)
model_path = os.path.join(model_dir, "model.joblib")
print(model_path)

loaded_model = joblib.load(model_path)
print(loaded_model)

model, targets = loaded_model
print(f"Model: {model}")
print(f"Targets: {targets}")

p = model.predict(["computer science lab wants a RAM, disk, computer"])
print(p)
print(targets[p[0]])
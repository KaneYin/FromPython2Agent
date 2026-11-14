from fastapi import FastAPI

from models.predictor import predict_species

app = FastAPI()

@app.get("/predict/")
def predict(bill: float, flipper: float):
    return {
        "parameters": {"bill_length": bill, "flipper_length": flipper},
        "result": predict_species(bill_length_mm=bill, flipper_length_mm=flipper),
    }

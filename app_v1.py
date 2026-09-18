import joblib
from fastapi import FastAPI

model = joblib.load("model.joblib")
app = FastAPI(title="Spam Detection API")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: dict):
    label = model.predict([payload["text"]])[0]
    return {"label": label}

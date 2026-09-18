import joblib
import os
import redis
import hashlib
from fastapi import FastAPI

model = joblib.load("model.joblib")
app = FastAPI(title="Spam Detection API")

redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "cache"), 
    port=int(os.environ.get("REDIS_PORT", 6379)), 
    decode_responses=True
)
TTL = int(os.environ.get("CACHE_TTL_SECONDS", 300))

@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": "v2"}

@app.post("/predict")
def predict(payload: dict):
    text = payload["text"]
    
    key = "predict:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
    
    cached = redis_client.get(key)
    if cached:
        print(f"[cache] HIT key={key}", flush=True)
        return {"label": cached}

    label = model.predict([text])[0]
    redis_client.set(key, label, ex=TTL)
    print(f"[cache] MISS key={key}", flush=True)    

    return {"label": label}

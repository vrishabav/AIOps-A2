import time
import requests

url = "http://localhost:8000/predict"
payload = {"text": "WIN a FREE iPhone now! Click here: bit.ly/xyz123"}

t0 = time.time()
r1 = requests.post(url, json=payload)
t1 = time.time()
r2 = requests.post(url, json=payload)
t2 = time.time()

print("Call 1 (cache MISS):", r1.json(), f"{(t1 - t0) * 1000:.2f} ms")
print("Call 2 (cache HIT): ", r2.json(), f"{(t2 - t1) * 1000:.2f} ms")

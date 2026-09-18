# Assignment 2 (DA3408 - AIOps)
### Vrishab Anurag Venkataraghavan (DA24B033)

A spam/ham classifier (TF-IDF + Multinomial Naive Bayes) served over FastAPI, containerized and deployed across four stages: Docker builds, Docker Compose + Redis caching, a Kubernetes Indexed Job, and a Kubernetes Deployment with self-healing and rolling updates.

## Repo layout

```
app.py                     API used for Q2 (Compose) and Q4 (k8s) - Redis-cached /predict
app_v1.py                  Original API without caching (Q1 baseline reference)
generate_random_dataset.py, train_model.py, model.joblib, spam_dataset.csv   shared training assets
requirements.txt

Dockerfile.singlestage     Q1 - naive single-stage build
Dockerfile.multistage      Q1 - builder + slim runtime multi-stage build
.dockerignore              Q1 - excludes data/log/evidence files from the build context

docker-compose.yml         Q2 - api + cache (redis) services
benchmark_cache.py         Q2 - MISS/HIT timing check

k8s/q3/                    Q3 - Indexed Job: generate_shards.py, validate_shard.py,
                            Dockerfile.validator, validate_shards.yaml, collect_shard_results.py, shards/
k8s/q4/                    Q4 - deployment.yaml, service.yaml, redis.yaml (cache for /predict on k8s)

evidence/                  captured command output per question (see index below)
writeup.md                 written answers/explanations, cited against evidence/
```

## How to run each part

**Q1 - Docker builds**
```
docker build -t spam-api-singlestage -f Dockerfile.singlestage .
docker build -t spam-api-multistage -f Dockerfile.multistage .
docker images spam-api-singlestage
docker images spam-api-multistage
```

**Q2 - Compose + Redis caching**
```
docker compose up --build -d
python benchmark_cache.py
docker compose down
```

**Q3 - Indexed Job (sharded validation)**
```
cd k8s/q3
kubectl apply -f validate_shards.yaml
kubectl get pods -o wide
python3 collect_shard_results.py
```

**Q4 - Deployment (self-healing + rolling update)**
```
cd k8s/q4
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f redis.yaml
curl http://$(minikube ip):30090/healthz
```
To demonstrate a rolling update: build a new image tagged `v2`, run `minikube image load spam-api:v2`, then `kubectl set image deployment/spam-api api=spam-api:v2` and watch `kubectl rollout status deployment/spam-api`.

## Evidence index

| File | What it proves |
|---|---|
| `evidence/q1_image_sizes.txt` | multi-stage image is smaller than single-stage |
| `evidence/q1_dockerignore_context.txt` | `.dockerignore` before/after build context |
| `evidence/q2_cache_benchmark.txt` | cache MISS vs HIT latency |
| `evidence/q3_job_pods.txt` | 8/8 shard pods completed, spread across nodes |
| `evidence/q3_shard_results.txt` | per-shard validation counts collected via the k8s API |
| `evidence/q4_selfheal.txt` | deleted pod auto-replaced by the ReplicaSet |
| `evidence/q4_rollout.txt` | v1→v2 rolling update status/history |
| `evidence/q4_predict_check.txt` | `/predict` works end-to-end on the k8s Deployment (with `cache` Service) |
| `evidence/q4_qos.txt` | resource requests/limits and resulting QoS class |

## AI disclosure

AI assistants (Claude and Gemini) were used during this assignment.
Uses included:
- Drafting boilerplate yaml files and this README structure (which has since been read through, verified and edited)
- Debugging Docker and Kubernetes errors encountered while running, including port conflicts, multi-stage `PATH` issues, multi-node image-loading behavior on minikube, `ErrImagePull` troubleshooting). Going through logs to verify correct implementation, or to debug unprecedented errors.
- Reviewing the repo for any gaps/discrepancies
- Understanding and implementing syntax for FastAPI, joblib etc (libraries I was previously unfamiliar with)
- Assisting in the writing of checking and data generation Python scripts

All commands were executed manually. All the output in `evidence/` and logs was captured on my machine. AI assistents were used as a debugging, verification and editing aid.

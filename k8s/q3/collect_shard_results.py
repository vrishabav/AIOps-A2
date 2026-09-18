import json, re
from kubernetes import client, config

RESULT_RE = re.compile(r"RESULT_JSON:(\{.*\})")

config.load_kube_config()
v1 = client.CoreV1Api()
pods = v1.list_namespaced_pod(namespace="default", label_selector="job-name=validate-shards-job")

rows = []
for pod in pods.items:
    logs = v1.read_namespaced_pod_log(pod.metadata.name, "default")
    m = RESULT_RE.search(logs)
    if m:
        rows.append(json.loads(m.group(1)))

rows.sort(key=lambda r: r["shard_index"])
for r in rows:
    print(r)
print("Total invalid rows across all shards:", sum(r["invalid_rows"] for r in rows))


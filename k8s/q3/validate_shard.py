import csv, json, os, re, socket

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

idx = int(os.environ.get("JOB_COMPLETION_INDEX", "0"))
pod_name = os.environ.get("POD_NAME", socket.gethostname())
node_name = os.environ.get("NODE_NAME", "unknown")

total, invalid = 0, 0
with open(f"/app/shards/shard_{idx}.csv") as f:
    for row in csv.DictReader(f):
        total += 1
        email, date = row.get("email", ""), row.get("signup_date", "")
        if not email or not EMAIL_RE.match(email) or not date:
            invalid += 1

result = {"shard_index": idx, "total_rows": total, "invalid_rows": invalid, "pod_name": pod_name, "node_name": node_name}
print("RESULT_JSON:" + json.dumps(result))

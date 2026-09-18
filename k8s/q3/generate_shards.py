import random, csv, os

random.seed(42)
os.makedirs("shards", exist_ok=True)

VALID_DOMAINS = ["example.com", "test.org", "mail.co"]
FIELDS = ["user_id", "email", "signup_date"]
N_SHARDS = 8
ROWS_PER_SHARD = 50


def make_row(i):
    invalid = random.random() < 0.2
    if not invalid:
        return [i, f"user{i}@{random.choice(VALID_DOMAINS)}", "2024-01-01"], False
    kind = random.choice(["bad_email", "missing_email", "missing_date"])
    if kind == "bad_email":
        email = f"user{i}AT{random.choice(VALID_DOMAINS)}"  # no '@'
        date = "2024-01-01"
    elif kind == "missing_email":
        email = ""
        date = "2024-01-01"
    else:
        email = f"user{i}@{random.choice(VALID_DOMAINS)}"
        date = ""
    return [i, email, date], True


for shard_idx in range(N_SHARDS):
    n_invalid = 0
    with open(f"shards/shard_{shard_idx}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS)
        for r in range(ROWS_PER_SHARD):
            row, invalid = make_row(shard_idx * ROWS_PER_SHARD + r)
            n_invalid += invalid
            writer.writerow(row)
    print(f"shard_{shard_idx}.csv -> {n_invalid} invalid rows (seeded)")


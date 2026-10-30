import hashlib, json

def step_hash(prev_hash, step):
    payload = json.dumps({"prev": prev_hash, "step": step}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()

def verify_chain(receipt):
    prev = "GENESIS"
    for step in receipt["steps"]:
        expected = step_hash(prev, {k: v for k, v in step.items() if k != "hash"})
        if expected != step["hash"]:
            return False, step.get("id", "?")
        prev = step["hash"]
    return True, None

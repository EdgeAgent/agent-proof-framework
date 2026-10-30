import json, os, time
from .chain import step_hash

GENESIS = "GENESIS"
BLOCKED = ("send", "ship", "pay", "delete", "merge")

class Receipt:
    def __init__(self, run_id, agent_id, task):
        self.run_id = run_id; self.agent_id = agent_id; self.task = task
        self.steps = []; self.prev = GENESIS; self.approvals = []
    def add(self, kind, detail, evidence=None, cost=0, approved_by=None):
        step = {"id": f"step-{len(self.steps)+1}", "kind": kind, "detail": detail,
                "evidence": evidence or "", "cost": cost, "approved_by": approved_by,
                "ts": int(time.time())}
        step["hash"] = step_hash(self.prev, step); self.prev = step["hash"]; self.steps.append(step); return step
    def gate(self, action, payload, approved=False, approver=None):
        if action in BLOCKED and not approved:
            self.add("gate_blocked", f"{action} blocked: {payload}", evidence="gate: exact approval required")
            return False
        self.add("gate_approved", f"{action} approved: {payload}", evidence="gate: exact payload approved", approved_by=approver)
        self.approvals.append({"action": action, "payload": payload, "approver": approver}); return True
    def fail_silent(self, detail):
        return self.add("failed_silent", detail, evidence="no output / no evidence — flagged, never silently passed")
    def to_dict(self):
        return {"run_id": self.run_id, "agent_id": self.agent_id, "task": self.task,
                "steps": self.steps, "approvals": self.approvals, "final_hash": self.prev,
                "total_cost": sum(s["cost"] for s in self.steps)}
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f: json.dump(self.to_dict(), f, indent=2)
        return path

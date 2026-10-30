import json, os
class Trust:
    """Trust compounds across runs: +1 per verified run, -3 per tampered/failed run. Never resets silently."""
    def __init__(self, path):
        self.path = path; self.scores = {}
        if os.path.exists(path):
            self.scores = json.load(open(path))
    def record(self, agent_id, verified):
        s = self.scores.get(agent_id, 50)
        self.scores[agent_id] = max(0, min(100, s + (1 if verified else -3)))
        json.dump(self.scores, open(self.path, "w"), indent=2); return self.scores[agent_id]

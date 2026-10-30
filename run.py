#!/usr/bin/env python3
"""PROOF demo CLI. Mock agents only, $0, no real model calls."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proof.receipt import Receipt
from proof.chain import verify_chain
from proof.trust import Trust

BASE = os.path.dirname(os.path.abspath(__file__))

def demo():
    r = Receipt("demo-1", "agent-orchestra-boss", "Build a lead pack for AgencyLead.ca")
    r.add("read", "Loaded 30 London no-website leads", evidence="london-ontario-no-website-leads.csv", cost=0)
    r.add("decision", "Scored leads, top 5 selected", evidence="score: A/B/C rubric", cost=0)
    r.add("tool", "Checked scrub list for top 5", evidence="scrub-list: 0 hits", cost=0)
    r.gate("send", "lead pack to client", approved=False)
    r.gate("send", "lead pack to client", approved=True, approver="Kevin")
    r.fail_silent("Agent-2 sub-task produced no output in 60s")
    path = r.save(os.path.join(BASE, "receipts", "demo-1.json"))
    print(f"Receipt: {path}\nSteps: {len(r.steps)}  Final hash: {r.prev[:16]}...  Cost: $0 (mock)")
    print("Gate: 1 blocked, 1 approved (Kevin, exact payload only)")
    print("Silent failure: 1 flagged, not passed")
    return path

def verify(path):
    receipt = json.load(open(path)); ok, bad = verify_chain(receipt)
    print(f"{'OK — chain intact, no tampering' if ok else f'TAMPERED at {bad} — do not trust this receipt'}")
    return ok

def proof(path):
    receipt = json.load(open(path)); ok, _ = verify_chain(receipt)
    rows = "".join(f"<tr><td>{s['id']}</td><td>{s['kind']}</td><td>{s['detail']}</td><td>{s['evidence']}</td></tr>" for s in receipt["steps"])
    html = f"""<!doctype html><html><head><meta charset=utf-8><title>PROOF — {receipt['run_id']}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:900px;margin:40px auto;padding:0 20px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px;text-align:left}}</style></head>
<body><h1>PROOF — Agent Receipt</h1><p>Run: {receipt['run_id']} | Agent: {receipt['agent_id']} | Task: {receipt['task']}</p>
<p><b>Verification: {'OK — chain intact' if ok else 'TAMPERED'}</b> | Final hash: {receipt['final_hash']} | Cost: ${receipt['total_cost']}</p>
<table><tr><th>Step</th><th>Kind</th><th>Detail</th><th>Evidence</th></tr>{rows}</table>
<p>Approvals: {json.dumps(receipt['approvals'])}</p><p>Static page, no animation, no login. Verify with: python3 run.py verify receipts/{receipt['run_id']}.json</p></body></html>"""
    out = os.path.join(os.path.dirname(path), "proof.html"); open(out, "w").write(html); print(f"Proof page: {out}"); return out

def tamper_demo():
    src = demo(); data = json.load(open(src)); data["steps"][1]["detail"] = "Scored leads, top 99 selected (TAMPERED)"
    out = os.path.join(BASE, "receipts", "demo-1-tampered.json"); json.dump(data, open(out, "w"), indent=2)
    print(f"Tampered copy: {out}"); verify(out)

def trust():
    t = Trust(os.path.join(BASE, "trust.json")); print(f"agent-orchestra-boss trust: {t.record('agent-orchestra-boss', True)}/100 (verified run: +1, tampered/failed: -3)")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    {"demo": demo, "verify": lambda: verify(sys.argv[2]), "proof": lambda: proof(sys.argv[2]),
     "tamper-demo": tamper_demo, "trust": trust}[cmd]()

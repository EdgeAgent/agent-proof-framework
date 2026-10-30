import sys, os, json, copy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from proof.receipt import Receipt
from proof.chain import verify_chain
from proof.trust import Trust

def test_chain_intact():
    r = Receipt("t1", "a1", "x"); r.add("read", "hello", evidence="e1"); assert verify_chain(r.to_dict())[0]
def test_tamper_detected():
    r = Receipt("t1", "a1", "x"); r.add("read", "hello"); d = r.to_dict(); d["steps"][0]["detail"] = "HACKED"; assert not verify_chain(d)[0]
def test_gate_blocks_unapproved():
    r = Receipt("t1", "a1", "x"); assert r.gate("send", "p", approved=False) is False; assert r.steps[-1]["kind"] == "gate_blocked"
def test_gate_approves_exact_only():
    r = Receipt("t1", "a1", "x"); assert r.gate("send", "p", approved=True, approver="Kevin") is True; assert r.approvals[0]["approver"] == "Kevin"
def test_silent_failure_flagged():
    r = Receipt("t1", "a1", "x"); r.fail_silent("no output"); assert r.steps[-1]["kind"] == "failed_silent"
def test_trust_compounds(tmp_path):
    t = Trust(str(tmp_path / "t.json")); assert t.record("a1", True) == 51; assert t.record("a1", False) == 48
if __name__ == "__main__":
    import tempfile, pathlib
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(pathlib.Path(tempfile.mkdtemp())) if "tmp_path" in fn.__code__.co_varnames else fn(); print(f"PASS {name}")
    print("ALL PASS")

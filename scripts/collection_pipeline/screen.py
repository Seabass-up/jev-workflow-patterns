"""Live screening driver: one uncached Jev call per fixture, receipts preserved as observed.

Append-only. A stored receipt is never replaced: a rerun screens only fixtures that have
no receipt yet, and each receipt is written to disk before the next call, so an
interrupted batch keeps every completed call. If a stored receipt no longer matches its
fixture state or contract, the run stops; change the contract by versioning it, never by
rescreening over the original evidence.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline_config import CLI, REPO  # noqa: E402


def call(state, questions):
    body = json.dumps({"state": state, "questions": questions})
    r = subprocess.run([CLI, "decide"], input=body, capture_output=True, text=True)
    if r.returncode != 0 and not r.stdout.strip():
        return {"ok": False, "advisory_only": True, "error": "cli_failure", "stderr": r.stderr[-300:]}
    return json.loads(r.stdout)


def write_atomic(path, receipts):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(receipts, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def load_receipts(path):
    return json.loads(path.read_text()) if path.exists() else []


def check_bindings(receipts, fixtures, patterns):
    """Stop if a stored receipt no longer matches its fixture state or contract."""
    fmap = {f["id"]: f for f in fixtures}
    for r in receipts:
        f = fmap.get(r["fixture_id"])
        if f is None:
            raise SystemExit("stored receipt %s has no fixture; receipts are never discarded" % r["fixture_id"])
        p = patterns[f["pattern_id"]]
        if r["request"]["state"] != f["state"] or r["request"]["questions"] != p["questions"] or r["version"] != p["version"]:
            raise SystemExit("stored receipt %s no longer matches its fixture or contract; version the contract "
                             "instead of rescreening over the original evidence" % r["fixture_id"])


def screen(collection, mode, root=None, caller=call):
    """Screen fixtures without a receipt; return the number of new calls made."""
    root = Path(root) if root else REPO / collection
    catalog = json.loads((root / "catalog.json").read_text())
    patterns = {p["id"]: p for p in catalog["patterns"]}
    fixtures = json.loads((root / "fixtures.json").read_text())
    (root / "results").mkdir(exist_ok=True)
    out = root / "results" / ("screening.json" if mode == "initial" else "recovery.json")
    receipts = load_receipts(out)
    check_bindings(receipts, fixtures, patterns)
    done = {r["fixture_id"] for r in receipts}
    if mode == "initial":
        targets = [f for f in fixtures if f["id"] not in done]
    else:
        initial = {r["fixture_id"]: r for r in load_receipts(root / "results/screening.json")}
        failed = [f for f in fixtures if f["id"] in initial and initial[f["id"]]["response"].get("ok") is False]
        targets = [f for f in failed if f["id"] not in done]
    if not targets:
        if not out.exists():
            write_atomic(out, receipts)
        print(collection, mode, "nothing to screen;", len(receipts), "stored receipts kept unchanged")
        return 0
    for f in targets:
        p = patterns[f["pattern_id"]]
        resp = caller(f["state"], p["questions"])
        receipts.append({"fixture_id": f["id"], "pattern_id": p["id"], "version": p["version"],
                         "request": {"state": f["state"], "questions": p["questions"], "model": resp.get("model", "jev-1.13.0")},
                         "response": resp})
        write_atomic(out, receipts)
        choice = resp.get("answers", {}).get("decision", {}).get("choice") if resp.get("ok") else resp.get("error")
        print(f["id"], f["expected"], "->", choice, "" if choice == f["expected"] else "  <-- differs")
    print(collection, mode, len(targets), "new receipts appended;", len(receipts) - len(targets), "stored receipts kept")
    return len(targets)


if __name__ == "__main__":
    screen(sys.argv[1], sys.argv[2])

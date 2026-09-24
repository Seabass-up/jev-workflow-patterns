"""Live screening driver: one uncached Jev call per fixture, receipts preserved as observed."""
import json
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


def screen(collection, mode):
    root = REPO / collection
    catalog = json.loads((root / "catalog.json").read_text())
    patterns = {p["id"]: p for p in catalog["patterns"]}
    fixtures = json.loads((root / "fixtures.json").read_text())
    out = root / "results" / ("screening.json" if mode == "initial" else "recovery.json")
    if mode == "initial":
        targets = fixtures
    else:
        initial = {r["fixture_id"]: r for r in json.loads((root / "results/screening.json").read_text())}
        targets = [f for f in fixtures if initial[f["id"]]["response"].get("ok") is False]
        if not targets:
            out.write_text("[]\n")
            print(collection, "no failures to recover")
            return
    receipts = []
    for f in targets:
        p = patterns[f["pattern_id"]]
        resp = call(f["state"], p["questions"])
        receipts.append({"fixture_id": f["id"], "pattern_id": p["id"], "version": p["version"],
                         "request": {"state": f["state"], "questions": p["questions"], "model": resp.get("model", "jev-1.13.0")},
                         "response": resp})
        choice = resp.get("answers", {}).get("decision", {}).get("choice") if resp.get("ok") else resp.get("error")
        print(f["id"], f["expected"], "->", choice, "" if choice == f["expected"] else "  <-- differs")
    out.write_text(json.dumps(receipts, indent=2, ensure_ascii=False) + "\n")
    print(collection, mode, len(receipts), "receipts written")


if __name__ == "__main__":
    screen(sys.argv[1], sys.argv[2])

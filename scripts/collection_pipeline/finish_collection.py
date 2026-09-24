"""Assemble a collection after authoring and challenge cases: fixtures, screen, evaluate, pages, wrappers.

Steps, run in order: merge | screen | finish
  merge  : design + challenge -> fixtures.json, validate structure and privacy tripwires.
           Refuses to change fixtures once any screening receipt exists.
  screen : one uncached Jev call per fixture without a receipt (initial), then one per
           provider failure (recovery). Append-only: stored receipts are never replaced.
  finish : summary.json, evaluate.py/test wrapper, kernel module copy, pages. Rebuilds
           derived files from the stored receipts, so it is safe to rerun.
"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline_config import REPO, WORKDIR as SCRATCH  # noqa: E402
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "discovery"))
from collection_tools import validate_collection  # noqa: E402
from check_candidates import PRIVATE  # noqa: E402


def merge(folder):
    root = REPO / folder
    catalog = json.loads((root / "catalog.json").read_text())
    pats = {p["id"]: p for p in catalog["patterns"]}
    design = json.loads((SCRATCH / f"design_{folder}.json").read_text())
    chal = json.loads((SCRATCH / f"challenge_{folder}.json").read_text())
    problems, fixtures = [], list(design)
    for c in chal:
        p = pats[c["pattern_id"]]
        if set(c["state"]) != set(p["required_state_fields"]):
            problems.append((c["pattern_id"], "fields", sorted(set(c["state"]) ^ set(p["required_state_fields"]))))
        if c["expected"] not in p["questions"]["decision"]["criteria"]:
            problems.append((c["pattern_id"], "label", c["expected"]))
        for k, v in c["state"].items():
            if v in ("", [], {}):
                problems.append((c["pattern_id"], "empty field", k))
        fixtures.append({"id": f"{c['pattern_id']}-4", "pattern_id": c["pattern_id"], "version": 1, "split": "challenge",
                         "author_origin": "independent_challenge_author", "state": c["state"], "expected": c["expected"],
                         "rationale": c["rationale"]})
    for f in fixtures:
        blob = json.dumps(f["state"], ensure_ascii=False)
        for rx, label in PRIVATE:
            if label == "email address":
                # Synthetic .example addresses are allowed in fixtures; anything else is not.
                if re.search(r"[\w.+-]+@[\w-]+\.(?!example\b)[\w.-]+", blob):
                    problems.append((f["id"], "private-looking", label))
            elif rx.search(blob):
                problems.append((f["id"], "private-looking", label))
        if re.search(r"@[\w-]+\.(com|net|org)\b", blob):
            problems.append((f["id"], "real TLD"))
    if problems:
        print(folder, "PROBLEMS", problems)
        return False
    fixtures.sort(key=lambda f: (f["pattern_id"], f["id"]))
    frozen = frozen_fixture_problem(root, fixtures)
    if frozen:
        print(folder, "REFUSED", frozen)
        return False
    (root / "fixtures.json").write_text(json.dumps(fixtures, indent=2, ensure_ascii=False) + "\n")
    validate_collection(catalog, fixtures, json.loads((root / "sources.json").read_text()))
    print(folder, "fixtures", len(fixtures), "validated")
    return True


def frozen_fixture_problem(root, fixtures):
    """Expectations are frozen once screened: any change would relabel stored evidence."""
    screened = root / "results/screening.json"
    current = root / "fixtures.json"
    if not screened.exists():
        return None
    if not current.exists() or json.loads(current.read_text()) != fixtures:
        return ("results/screening.json exists, so fixtures.json is frozen; "
                "version the affected contract and add new fixtures instead of rewriting these")
    return None


def screen(folder):
    for mode in ("initial", "recovery"):
        r = subprocess.run([sys.executable, str(HERE / "screen.py"), folder, mode], capture_output=True, text=True, cwd=REPO)
        lines = [l for l in r.stdout.splitlines() if "differs" in l or "appended" in l or "nothing to screen" in l or "->" in l and "error" in l.lower()]
        print("\n".join(lines) if lines else r.stdout[-300:])
        if r.returncode != 0:
            print(r.stderr[-500:])
            return False
    return True


def finish(folder):
    root = REPO / folder
    for name in ("evaluate.py", "test_evaluate.py"):
        shutil.copy(REPO / "controls" / name, root / name)
    (root / "results").mkdir(exist_ok=True)
    (root / "patterns").mkdir(exist_ok=True)
    spec = importlib.util.spec_from_file_location(folder + "_ev", root / "evaluate.py")
    ev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ev)
    summary_path = root / "results/summary.json"
    if summary_path.exists():
        summary_path.unlink()
    from collection_tools import report
    result = report(root)
    summary_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    r = subprocess.run([sys.executable, str(root / "evaluate.py")], capture_output=True, text=True, cwd=REPO)
    if r.returncode != 0:
        print(folder, "REPLAY FAILED", r.stderr[-400:])
        return False
    module = SCRATCH / f"module_{folder}.md"
    shutil.copy(module, REPO / "skills/jev-question-kernel-catalog/references" / f"{folder}.md")
    r = subprocess.run([sys.executable, str(REPO / "scripts/build_collection_pages.py"), folder], capture_output=True, text=True, cwd=REPO)
    print(r.stdout.strip() or r.stderr[-400:])
    s = result["splits"]
    print(folder, "design %d/%d challenge %d/%d provisional %s failures %s" % (
        s["design"]["label_matches"], s["design"]["cases"], s["challenge"]["label_matches"], s["challenge"]["cases"],
        result["provisional_patterns"], result["initial_provider_failures"]))
    return True


if __name__ == "__main__":
    step, folders = sys.argv[1], sys.argv[2:]
    ok = all({"merge": merge, "screen": screen, "finish": finish}[step](f) for f in folders)
    raise SystemExit(0 if ok else 1)

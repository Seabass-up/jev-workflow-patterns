"""Inventory every profile and replay all local suites; no network or action calls.

An inventory row is not semantic approval. New review runs are immutable snapshots.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def catalogs(root=ROOT):
    return sorted([*root.glob("*/catalog.json"), *root.glob("iterations/[0-9][0-9]/catalog.json")])


def inventory(root=ROOT):
    rows = []
    for path in catalogs(root):
        data = json.loads(path.read_text())
        seen = set()
        for pattern in data["patterns"]:
            pid = pattern["id"]
            if pid in seen:
                raise ValueError("duplicate pattern ID in " + str(path))
            seen.add(pid)
            version = pattern.get("version", pattern.get("contract_version"))
            if type(version) is not int or version < 1:
                raise ValueError("invalid version for " + pid)
            payload = json.dumps(pattern, sort_keys=True, ensure_ascii=False, allow_nan=False,
                                 separators=(",", ":")).encode()
            rows.append({"key": str(path.parent.relative_to(root)) + "/" + pid,
                         "catalog": str(path.relative_to(root)), "id": pid,
                         "version": version,
                         "version_field": "version" if "version" in pattern else "contract_version",
                         "pattern_sha256": hashlib.sha256(payload).hexdigest(),
                         "question_count": len(pattern["questions"]),
                         "semantic_review": "pending", "live_boundary_test": "pending"})
    return rows


def commands(root=ROOT):
    result = []
    folders = [p.parent for p in catalogs(root)]
    for folder in folders:
        result.extend([[sys.executable, str(folder / "evaluate.py")],
                       [sys.executable, "-m", "unittest", "discover", "-s", str(folder), "-p", "test_*.py"]])
    for folder in ("scripts", "scripts/collection_pipeline", "skills/jev-question-kernel-catalog/scripts", "discovery"):
        result.append([sys.executable, "-m", "unittest", "discover", "-s", str(root / folder), "-p", "test_*.py"])
    result.append([sys.executable, str(root / "pilots/github-issue-routing/verify_pilot.py")])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; preserve prior runs")
    rows = inventory()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    checks = []
    for command in commands():
        completed = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        checks.append({"command": [v.replace(str(ROOT), ".") for v in command],
                       "returncode": completed.returncode, "stdout": completed.stdout,
                       "stderr": completed.stderr})
    report = {"observed_at": datetime.now(timezone.utc).isoformat(),
              "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "profile_count": len(rows), "catalog_count": len(catalogs()),
              "foundational_guides": [str(p.relative_to(ROOT)) for p in sorted((ROOT / "patterns").glob("*.md"))],
              "patterns": rows, "checks": checks,
              "scope": "Recorded-response replay and existing tests only; semantic and live boundary review pending."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents replacing an earlier run even if another process raced.
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    failed = [c["command"] for c in checks if c["returncode"]]
    print(json.dumps({"profiles": len(rows), "catalogs": len(catalogs()), "checks": len(checks), "failed": failed}))
    return bool(failed)


if __name__ == "__main__":
    raise SystemExit(main())

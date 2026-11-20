"""Read-only integrity check/loader for the pinned research supplement.

No inference, consumer execution, release rebuild, or source-worktree writes.
Hashes detect drift relative to this manifest; they are not an authenticity proof.
This is a fixed import, not a general mechanism for admitting new patterns.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess


DEFAULT_BUNDLE = Path(__file__).resolve().parents[1] / "assets/research-edition"
SOURCE_COMMIT = "48a8b4569a9ce5b17ce1119d63179e84a2990ae6"
VERSIONS = {f"JP-{n:03d}": 2 if n == 11 else 1 for n in (2, 3, 4, 5, 7, 8, 10, 11, 12, 13)}
EXCLUDED = {"JP-001": (1, "AUDIT_HOLD"), "JP-006": (1, "HELD"),
            "JP-009": (1, "HELD"), "JP-014": (2, "HELD")}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError(f"Non-finite JSON value: {value}")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject_constant)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def relative_path(value):
    require(isinstance(value, str) and bool(value), "Missing relative path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value and
            all(part not in {".", ".."} for part in path.parts) and "\\" not in value,
            f"Not a normalized relative path: {value}")
    return path


def local_file(root, relative):
    path = relative_path(relative)
    candidate = root
    for part in path.parts:
        candidate = candidate / part
        require(not candidate.is_symlink(), f"Symlink is not a bundled file: {relative}")
    require(candidate.is_file(), f"Missing regular file: {relative}")
    return candidate


def keyed_rows(rows, expected, label):
    require(isinstance(rows, list), f"{label} must be a list")
    result = {}
    for row in rows:
        require(isinstance(row, dict) and isinstance(row.get("id"), str), f"Invalid {label} row")
        require(row["id"] not in result, f"Duplicate {label} ID: {row['id']}")
        result[row["id"]] = row
    require(set(result) == set(expected), f"{label} ID coverage differs from the frozen snapshot")
    return result


def verify_source(manifest, source_root):
    """Compare Git objects, not a moving worktree or a historical release builder."""
    root = Path(source_root).resolve()
    source = manifest["source"]
    original = {}
    for name, expected in source["files"].items():
        relative_path(name)
        result = subprocess.run(["git", "show", f"{SOURCE_COMMIT}:{name}"], cwd=root,
                                capture_output=True, check=False)
        require(result.returncode == 0, f"Cannot read pinned source object: {name}")
        require(digest(result.stdout) == expected, f"Pinned source hash mismatch: {name}")
        original[name] = result.stdout
    index = strict_json(original["catalog/agent-index.json"])["families"]
    accepted = strict_json(original["catalog/accepted.json"])["patterns"]
    admitted = keyed_rows(accepted, VERSIONS, "source admissions")
    challenges = {row["id"]: row for row in strict_json(original["audit/challenge-results.json"])["patterns"]}
    challenges["JP-013"] = strict_json(original["research/academic-expansion/runs/JP-013.challenge.results.json"])
    for row in manifest["patterns"]:
        origin = index[row["family"]]
        require((origin["pattern_id"], origin["version"], origin["status"], origin["contract"], origin["consumer"])
                == (row["id"], row["version"], row["status"], row["source_contract"], row["source_consumer"]),
                f"Source index mismatch: {row['id']}")
        for key, result in (("development", admitted[row["id"]]),
                            ("same_author_fresh_challenge", challenges[row["id"]])):
            require(row["evidence"][key] == {"correct": result["correct"], "total": result["total"]},
                    f"Source result summary mismatch: {row['id']}")
    return len(original)


def load_bundle(bundle=DEFAULT_BUNDLE, source_root=None):
    root = Path(bundle).resolve()
    manifest = strict_json(local_file(root, "manifest.json").read_bytes())
    require(manifest.get("schema_version") == 1, "Unsupported import schema")
    require(manifest.get("model") == "jev-1.13.0", "Snapshot model changed")
    require(manifest.get("evidence_grade") == "synthetic_development_and_same_author_fresh_challenge",
            "Snapshot evidence grade changed")
    for field in ("production_qualified", "specialist_qualification", "consumers_bundled"):
        require(manifest.get(field) is False, f"Unwarranted import claim: {field}")
    source = manifest["source"]
    require(source["commit"] == SOURCE_COMMIT and source["goal_status_at_checkpoint"] == "paused_incomplete"
            and source["final_project_audit"] == "pending", "Checkpoint boundary changed")
    require(isinstance(source["files"], dict) and source["files"], "Missing source hash map")
    for path, sha in source["files"].items():
        relative_path(path)
        require(isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha), f"Invalid SHA-256: {path}")
    rows = keyed_rows(manifest["patterns"], VERSIONS, "admissions")
    excluded = keyed_rows(manifest["excluded"], EXCLUDED, "exclusions")
    for key, (version, status) in EXCLUDED.items():
        require((excluded[key]["version"], excluded[key]["status"]) == (version, status),
                f"Exclusion changed: {key}")
    working = keyed_rows(manifest["working_additions"], {"JP-017"}, "working additions")["JP-017"]
    require(working["included"] is False and working["audit_status"] == "PENDING"
            and working["source_status"] == "ACCEPTED_RESEARCH" and working["version"] == 1,
            "Working addition silently promoted or relabeled")
    coverage = manifest["coverage_at_checkpoint"]
    require((coverage["academic_routes"], coverage["individual_mixed_transfer_screen"],
             coverage["no_individual_transfer_screen"], coverage["individual_domain_validation"],
             coverage["domain_status"], coverage["occupations"], coverage["rated_task_statements"])
            == (155, 22, 133, 0, "UNSCREENED", 50, 211), "Checkpoint discovery/domain distinction changed")
    transfer = manifest["jp002_public_transfer"]
    require((transfer["status"], transfer["split"], transfer["correct"], transfer["total"],
             transfer["read_only_previews"], transfer["reviews"], transfer["public_previews"],
             transfer["wrong_previews"], transfer["baseline_public_previews"])
            == ("TRANSFER_SCREEN_PASS", "development_screen", 12, 12, 9, 3, 5, 0, 0),
            "Historical transfer summary changed")
    contracts = {}
    for key, row in rows.items():
        require(type(row["version"]) is int and row["version"] == VERSIONS[key], f"Version changed: {key}")
        require(row["status"] == "ACCEPTED_RESEARCH" and
                row["allowed_use"] == "bounded_advisory_trial_with_application_owned_consumer",
                f"Invalid admission boundary: {key}")
        require(row["contract"] == f"contracts/{key}.v{row['version']}.json", f"Contract path changed: {key}")
        raw = local_file(root, row["contract"]).read_bytes()
        require(digest(raw) == row["sha256"] == source["files"][row["source_contract"]],
                f"Contract hash mismatch: {key}")
        require(row["source_consumer"] in source["files"], f"Unbound source consumer: {key}")
        contract = strict_json(raw)
        require((contract["contract_id"], contract["version"], contract["family"], contract["title"])
                == (key, row["version"], row["family"], row["title"]), f"Contract metadata mismatch: {key}")
        fields = row["required_state_fields"]
        require(isinstance(fields, list) and fields and all(isinstance(f, str) and f for f in fields)
                and len(set(fields)) == len(fields), f"Invalid input-field guidance: {key}")
        # Questions are retained byte-for-byte; this is not the authoring-envelope schema.
        require(isinstance(contract["request"]["questions"], dict) and contract["request"]["questions"],
                f"Missing complete questions: {key}")
        require(row["evidence"] == {"development": {"correct": 12, "total": 12},
                                   "same_author_fresh_challenge": {"correct": 6, "total": 6}},
                f"Frozen evidence summary changed: {key}")
        contracts[key] = contract
    actual = {p.relative_to(root).as_posix() for p in (root / "contracts").rglob("*") if p.is_file() or p.is_symlink()}
    require(actual == {row["contract"] for row in rows.values()}, "Unregistered or missing bundled contract")
    if source_root is not None:
        verify_source(manifest, source_root)
    return manifest, contracts


def load_contract(pattern_id, bundle=DEFAULT_BUNDLE):
    _, contracts = load_bundle(bundle)
    require(pattern_id in contracts, f"Not in this admitted snapshot: {pattern_id}")
    return contracts[pattern_id]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--source-root", type=Path, help="Optional local source repository; checks pinned Git objects only")
    parser.add_argument("--show", help="Print one admitted contract; never submits it")
    args = parser.parse_args()
    try:
        manifest, contracts = load_bundle(args.bundle, args.source_root)
        if args.show:
            require(args.show in contracts, f"Not in this admitted snapshot: {args.show}")
            result = {"advisory_only": True, "source_commit": SOURCE_COMMIT, "contract": contracts[args.show]}
        else:
            result = {"ok": True, "check": "import_integrity_only", "patterns": len(contracts),
                      "excluded": len(manifest["excluded"]), "pending_not_imported": ["JP-017"],
                      "source_commit": SOURCE_COMMIT, "source_git_objects_checked": args.source_root is not None,
                      "production_qualified": False, "consumer_execution": False, "provider_calls": 0}
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.exit(1, f"Research import rejected: {error}\n")


if __name__ == "__main__":
    main()

"""Inspect a fixed audit-pending research import; explicitly opt in to display it.

This loader never calls a model, runs a consumer or admits a production pattern.
Its hash anchor detects drift within a trusted skill copy, not source authenticity.
A new research checkpoint requires a separately reviewed import and new anchor.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import json

from check_research_import import digest, keyed_rows, local_file, relative_path, require, strict_json


DEFAULT_BUNDLE = Path(__file__).resolve().parents[1] / "assets/research-working"
SOURCE_COMMIT = "cb69774a6a9669ff412511094bebb387b382d008"
MANIFEST_SHA256 = "18e9e72079ff4eb94e11d8737f7814fb3b3635abcd256a326290f6e37dc36d9e"
VERSIONS = {"JP-001": 4, "JP-017": 1, "JP-019": 1, "JP-021": 2,
            "JP-023": 2, "JP-025": 1, "JP-026": 1, "JP-027": 1,
            "JP-028": 1, "JP-031": 1, "JP-033": 1, "JP-035": 1,
            "JP-036": 1, "JP-038": 1, "JP-039": 1, "JP-040": 1,
            "JP-042": 1, "JP-045": 1, "JP-046": 1}


def question_for(contract):
    """Preserve JP-017's different source envelope without rewriting its bytes."""
    if contract["contract_id"] == "JP-017":
        return contract["request"]["question_template"]
    return contract["question"]


def verify_source(manifest, source_root):
    root = Path(source_root).resolve()
    for name, expected in manifest["source"]["files"].items():
        relative_path(name)
        result = subprocess.run(["git", "show", f"{SOURCE_COMMIT}:{name}"], cwd=root,
                                capture_output=True, check=False)
        require(result.returncode == 0, f"Cannot read pinned source object: {name}")
        require(digest(result.stdout) == expected, f"Pinned source hash mismatch: {name}")
    return len(manifest["source"]["files"])


def inspect_bundle(bundle=DEFAULT_BUNDLE, source_root=None):
    root = Path(bundle).resolve()
    raw = local_file(root, "manifest.json").read_bytes()
    # Check strict JSON as well as the committed, code-owned digest. Updating a
    # manifest's own hash map cannot silently admit different contracts or claims.
    manifest = strict_json(raw)
    require(digest(raw) == MANIFEST_SHA256, "Frozen manifest changed")
    require(manifest["schema_version"] == 1 and
            manifest["source"]["commit"] == SOURCE_COMMIT and
            manifest["project_audit_status"] == "AUDIT_PENDING", "Import boundary changed")
    for field in ("production_qualified", "specialist_qualification", "consumers_bundled",
                  "inference_receipts_bundled", "model_quality_retested_by_import"):
        require(manifest[field] is False, f"Unwarranted import claim: {field}")
    assets = {}
    for name, expected in manifest["bundled_files"].items():
        payload = local_file(root, name).read_bytes()
        require(digest(payload) == expected, f"Bundled file hash mismatch: {name}")
        assets[name] = strict_json(payload) if name.endswith(".json") else payload.decode("utf-8")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*")
              if p.is_file() or p.is_symlink()}
    require(actual == set(assets) | {"manifest.json"}, "Unregistered or missing bundled file")

    admissions = assets[manifest["admissions_file"]]
    require(admissions["project_audit_status"] == "PENDING", "Source audit status changed")
    admitted = keyed_rows(admissions["patterns"], VERSIONS, "source working additions")
    rows = keyed_rows(manifest["patterns"], VERSIONS, "imported working additions")
    for pid, row in rows.items():
        require(type(row["version"]) is int and row["version"] == VERSIONS[pid]
                and row["selector"] == f"{pid}@{row['version']}", f"Version changed: {pid}")
        source_row = admitted[pid]
        require(source_row["version"] == row["version"] and
                source_row["status"] == row["source_status"] == "ACCEPTED_RESEARCH"
                and row["audit_status"] == "AUDIT_PENDING", f"Admission boundary changed: {pid}")
        require(row["contract"] == f"contracts/{pid}.v{row['version']}.json", f"Path changed: {pid}")
        require(row["sha256"] == manifest["bundled_files"][row["contract"]]
                == manifest["source"]["files"][row["source_contract"]], f"Source binding changed: {pid}")
        require(row["source_consumer"] in manifest["source"]["files"], f"Unbound consumer: {pid}")
        contract = assets[row["contract"]]
        require((contract["contract_id"], contract["version"], contract["title"])
                == (pid, row["version"], row["title"]), f"Contract identity changed: {pid}")
        require(contract["required_state_fields"] == row["required_state_fields"],
                f"Input guidance changed: {pid}")
        question = question_for(contract)
        require(question["type"] == "choice" and question["instructions"]
                and isinstance(question["criteria"], dict) and len(question["criteria"]) >= 2,
                f"Incomplete question: {pid}")
    composition = keyed_rows(manifest["compositions"], {"AP-C01"}, "compositions")["AP-C01"]
    require(composition["component_contracts"] == ["JP-025@1", "JP-023@2"]
            and composition["kind"] == "composition_not_new_primitive"
            and composition["audit_status"] == "AUDIT_PENDING", "Composition boundary changed")
    require(assets[composition["contract"]]["component_contracts"] == composition["component_contracts"],
            "Composition components changed")
    if source_root is not None:
        verify_source(manifest, source_root)
    return manifest, assets


def load_contract(selector, *, allow_audit_pending=False, bundle=DEFAULT_BUNDLE,
                  composition=False, source_root=None):
    """Return a marked envelope, never a bare question or an executable consumer.

    The flag is a caller acknowledgement of evidence limits, not user permission.
    Exact ID@version is required; held/unknown versions have no fallback.
    """
    require(allow_audit_pending is True, "Explicit allow_audit_pending=True is required")
    manifest, assets = inspect_bundle(bundle, source_root)
    rows = manifest["compositions" if composition else "patterns"]
    selected = next((row for row in rows if row["selector"] == selector), None)
    require(selected is not None, f"Not an exact selectable research version: {selector}")
    result = {"advisory_only": True, "audit_status": "AUDIT_PENDING",
              "production_qualified": False, "source_commit": SOURCE_COMMIT,
              "consumer_execution": False, "action": "none", "provider_calls": 0,
              "kind": "composition_not_new_primitive" if composition else "research_working_contract",
              "provenance": selected, "contract": assets[selected["contract"]]}
    if not composition:
        result["source_admission"] = next(row for row in assets["admissions.json"]["patterns"]
                                          if row["id"] == selected["id"])
    else:
        result["source_admission"] = assets["compositions.md"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--source-root", type=Path, help="Verify pinned Git blobs, never moving source files")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--show", metavar="ID@VERSION", help="Display one audit-pending question contract")
    selection.add_argument("--show-composition", metavar="ID@VERSION", help="Display a composition separately")
    parser.add_argument("--allow-audit-pending", action="store_true",
                        help="Acknowledge research-only status when displaying a contract")
    args = parser.parse_args()
    try:
        if args.show or args.show_composition:
            result = load_contract(args.show or args.show_composition,
                                   allow_audit_pending=args.allow_audit_pending,
                                   bundle=args.bundle, composition=bool(args.show_composition),
                                   source_root=args.source_root)
        else:
            manifest, _ = inspect_bundle(args.bundle, args.source_root)
            result = {"ok": True, "check": "import_integrity_only", "audit_status": "AUDIT_PENDING",
                      "source_commit": SOURCE_COMMIT, "patterns": len(manifest["patterns"]),
                      "compositions": len(manifest["compositions"]),
                      "selectors": [row["selector"] for row in manifest["patterns"]],
                      "source_git_objects_checked": len(manifest["source"]["files"]) if args.source_root else 0,
                      "production_qualified": False, "consumer_execution": False, "provider_calls": 0}
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.exit(1, f"Research working import rejected: {error}\n")


if __name__ == "__main__":
    main()

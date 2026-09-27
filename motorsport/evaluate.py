"""Replay the original and revised synthetic motorsport receipts offline."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "scripts"))
from collection_tools import replay as replay_collection, unique, validate_collection, validate_receipt  # noqa: E402,F401


def read(path):
    """Read a JSON file relative to this collection."""
    return json.loads((ROOT / path).read_text())


def valid_version(value):
    return type(value) is int and value > 0


def validate_pattern_history(old_patterns, patterns):
    before, after = unique(old_patterns, "id"), unique(patterns, "id")
    if set(before) != set(after):
        raise ValueError("pattern identity changed")
    revised = set()
    for pid, original in before.items():
        current = after[pid]
        if not valid_version(original.get("version")) or not valid_version(current.get("version")):
            raise ValueError("invalid pattern version")
        if original["version"] == current["version"]:
            if original != current:
                raise ValueError("pattern changed without a version increment")
            continue
        if current["version"] != original["version"] + 1:
            raise ValueError("pattern version must increment exactly once")
        old_content = {k: v for k, v in original.items() if k != "version"}
        new_content = {k: v for k, v in current.items() if k != "version"}
        if old_content == new_content:
            raise ValueError("contract version changed without a content change")
        revised.add(pid)
    return revised


def validate_fixture_history(old_fixtures, fixtures, revised_pattern_ids, patterns):
    before, after = unique(old_fixtures, "id"), unique(fixtures, "id")
    pattern_map = unique(patterns, "id")
    if any(not valid_version(f.get("version")) for f in old_fixtures + fixtures):
        raise ValueError("invalid fixture version")
    if not set(before).issubset(after):
        raise ValueError("frozen fixture removed")
    for fid, original in before.items():
        current = after[fid]
        old_content = {k: v for k, v in original.items() if k != "version"}
        current_content = {k: v for k, v in current.items() if k != "version"}
        if old_content != current_content:
            raise ValueError("frozen fixture was rewritten")
    added = set(after) - set(before)
    if not added:
        raise ValueError("revision must add a fresh boundary fixture")
    for pid in revised_pattern_ids:
        if not any(after[fid]["pattern_id"] == pid for fid in added):
            raise ValueError("each revised pattern must add a fresh boundary fixture")
    for fid, fixture in after.items():
        pattern = pattern_map.get(fixture["pattern_id"])
        if pattern is None or fixture["version"] != pattern["version"]:
            raise ValueError("fixture version does not match current contract")
        if fid in added and fixture["pattern_id"] not in revised_pattern_ids:
            raise ValueError("new fixture must target a revised contract")


def report():
    catalog, fixtures = read("catalog.json"), read("fixtures.json")
    sources = read("sources.json")
    initial_catalog = read("results/initial-catalog.json")
    initial_fixtures = read("results/initial-fixtures.json")
    initial_screen = read("results/screening.json")
    initial_recovery = read("results/recovery.json")
    refinement = read("results/refinement.json")
    refinement_recovery = read("results/refinement-recovery.json")

    revised_ids = validate_pattern_history(initial_catalog["patterns"], catalog["patterns"])
    validate_fixture_history(initial_fixtures, fixtures, revised_ids, catalog["patterns"])

    initial = replay_collection(
        initial_catalog, initial_fixtures, sources, initial_screen, initial_recovery
    )
    if initial != read("results/initial-summary.json"):
        raise ValueError("archived initial summary differs from its receipts")

    current_patterns = unique(catalog["patterns"], "id")
    refinement_patterns = [current_patterns[pid] for pid in sorted(revised_ids)]
    refinement_fixtures = [f for f in fixtures if f["pattern_id"] in revised_ids]
    refinement_summary = replay_collection(
        {**catalog, "patterns": refinement_patterns},
        refinement_fixtures,
        sources,
        refinement,
        refinement_recovery,
    )
    refinement_summary["scope"] = (
        "Three preserved synthetic design fixtures and three challenge-split cases, "
        "including MR04-4 from the original challenge and two reviewer-authored additions; "
        "not held-out accuracy or production qualification."
    )

    current_screen = [
        r for r in initial_screen if r["pattern_id"] not in revised_ids
    ] + refinement
    current_recovery = [
        r for r in initial_recovery if r["pattern_id"] not in revised_ids
    ] + refinement_recovery
    current = replay_collection(
        catalog, fixtures, sources, current_screen, current_recovery
    )
    current["scope"] = (
        "Synthetic current selection combines unchanged v1 cases with MR04 v2 receipts; "
        "MR04-5 and MR04-6 were added by the contract reviewer, not independently or held out. "
        "No production accuracy, calibration, or domain qualification claim."
    )

    runs = initial_screen + initial_recovery + refinement + refinement_recovery
    successful = [r for r in runs if r["response"].get("ok") is True]
    return {
        "initial": initial,
        "refinement": refinement_summary,
        "current": current,
        "request_digests_verified": len(successful),
        "provider_input_tokens": sum(
            r["response"]["usage"]["input_tokens"] for r in successful
        ),
        "provider_output_tokens": sum(
            r["response"]["usage"]["output_tokens"] for r in successful
        ),
        "bridge_estimated_cost_usd": round(
            sum(r["response"]["estimated_cost_usd"] for r in successful), 10
        ),
        "models": sorted({r["response"]["model"] for r in successful}),
        "revision": {
            "patterns": sorted(revised_ids),
            "new_fixture_ids": sorted(
                set(f["id"] for f in fixtures) - set(f["id"] for f in initial_fixtures)
            ),
        },
        "scope": (
            "Synthetic author-labelled design and challenge screens; not held-out "
            "production accuracy, calibration, or domain qualification."
        ),
    }


if __name__ == "__main__":
    result = report()
    print(json.dumps(result, indent=2))
    if result != read("results/summary.json"):
        raise SystemExit("saved summary differs from replay")

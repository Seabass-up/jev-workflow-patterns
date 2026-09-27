"""Replay original and versioned construction screening receipts offline."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "scripts"))
from collection_tools import (  # noqa: E402,F401
    digest,
    replay as replay_collection,
    unique,
    validate_collection,
    validate_receipt,
)


def read(path):
    """Read a JSON file relative to this collection."""
    return json.loads((ROOT / path).read_text())


def valid_version(value):
    return type(value) is int and value > 0


def current_fixtures(catalog, fixtures):
    """Return only fixtures whose immutable version matches the current contract."""
    patterns = unique(catalog["patterns"], "id")
    return [
        fixture for fixture in fixtures
        if fixture["version"] == patterns[fixture["pattern_id"]]["version"]
    ]


def validate_pattern_history(old_patterns, patterns):
    before, after = unique(old_patterns, "id"), unique(patterns, "id")
    if set(before) != set(after):
        raise ValueError("pattern identity changed")
    revised = set()
    for pattern_id, original in before.items():
        current = after[pattern_id]
        if not valid_version(original.get("version")) or not valid_version(current.get("version")):
            raise ValueError("invalid pattern version")
        if original["version"] == current["version"]:
            if original != current:
                raise ValueError("pattern changed without a version increment")
            continue
        if current["version"] != original["version"] + 1:
            raise ValueError("pattern version must increment exactly once")
        old_content = {key: value for key, value in original.items() if key != "version"}
        new_content = {key: value for key, value in current.items() if key != "version"}
        if old_content == new_content:
            raise ValueError("contract version changed without a content change")
        revised.add(pattern_id)
    return revised


def validate_fixture_history(old_fixtures, fixtures, revised_pattern_ids, old_patterns, patterns):
    """Keep superseded expectations immutable while screening only current-version cases."""
    before, after = unique(old_fixtures, "id"), unique(fixtures, "id")
    old_pattern_map, pattern_map = unique(old_patterns, "id"), unique(patterns, "id")
    if any(not valid_version(fixture.get("version")) for fixture in old_fixtures + fixtures):
        raise ValueError("invalid fixture version")
    if not set(before).issubset(after):
        raise ValueError("frozen fixture removed")
    for fixture_id, original in before.items():
        current = after[fixture_id]
        if original != current:
            raise ValueError("frozen fixture was rewritten")
        old_pattern = old_pattern_map.get(original["pattern_id"])
        if old_pattern is None or original["version"] != old_pattern["version"]:
            raise ValueError("archived fixture is not bound to its original contract")

    added_ids = set(after) - set(before)
    for fixture_id in added_ids:
        fixture = after[fixture_id]
        pattern = pattern_map.get(fixture["pattern_id"])
        if pattern is None or fixture["pattern_id"] not in revised_pattern_ids:
            raise ValueError("new fixture must target a revised pattern")
        if fixture["version"] != pattern["version"]:
            raise ValueError("new fixture must use the revised contract version")

    for pattern_id, pattern in pattern_map.items():
        active = [
            fixture for fixture in fixtures
            if fixture["pattern_id"] == pattern_id and fixture["version"] == pattern["version"]
        ]
        if pattern_id in revised_pattern_ids:
            design_count = sum(fixture["split"] == "design" for fixture in active)
            challenge_count = sum(fixture["split"] == "challenge" for fixture in active)
            if len(active) < 4 or design_count < 3 or challenge_count < 1:
                raise ValueError("revised pattern needs three design and one challenge case")
            if not any(fixture["id"] in added_ids for fixture in active):
                raise ValueError("each revised pattern needs new versioned fixtures")
            if any(fixture["id"] in before for fixture in active):
                raise ValueError("superseded fixtures cannot be relabeled as current-version cases")
        elif any(fixture["id"] in added_ids for fixture in active):
            raise ValueError("new fixture must target a revised pattern")
    return added_ids


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
    added_fixture_ids = validate_fixture_history(
        initial_fixtures, fixtures, revised_ids,
        initial_catalog["patterns"], catalog["patterns"],
    )
    active_fixtures = current_fixtures(catalog, fixtures)

    initial = replay_collection(
        initial_catalog, initial_fixtures, sources, initial_screen, initial_recovery
    )
    if initial != read("results/initial-summary.json"):
        raise ValueError("archived initial summary differs from its receipts")

    patterns = unique(catalog["patterns"], "id")
    refinement_patterns = [patterns[pattern_id] for pattern_id in sorted(revised_ids)]
    refinement_fixtures = [
        fixture for fixture in active_fixtures if fixture["pattern_id"] in revised_ids
    ]
    refinement_summary = replay_collection(
        {**catalog, "patterns": refinement_patterns},
        refinement_fixtures,
        sources,
        refinement,
        refinement_recovery,
    )
    refinement_summary["scope"] = (
        "Seven reviewer-authored CN05 v2 synthetic cases (three design and four challenge); "
        "the challenge cases are development screens, not independently labeled or held out."
    )

    current_screen = [
        receipt for receipt in initial_screen if receipt["pattern_id"] not in revised_ids
    ] + refinement
    current_recovery = [
        receipt for receipt in initial_recovery if receipt["pattern_id"] not in revised_ids
    ] + refinement_recovery
    current = replay_collection(
        catalog, active_fixtures, sources, current_screen, current_recovery
    )
    current["scope"] = (
        "Current synthetic selection combines unchanged version-1 contracts with CN05 v2; "
        "the original CN05 v1 miss remains in the initial history and is not relabeled. "
        "No production accuracy, calibration, safety decision, or domain qualification claim."
    )

    runs = initial_screen + initial_recovery + refinement + refinement_recovery
    successful = [receipt for receipt in runs if receipt["response"].get("ok") is True]
    return {
        "initial": initial,
        "refinement": refinement_summary,
        "current": current,
        "request_digests_verified": len(successful),
        "provider_input_tokens": sum(
            receipt["response"]["usage"]["input_tokens"] for receipt in successful
        ),
        "provider_output_tokens": sum(
            receipt["response"]["usage"]["output_tokens"] for receipt in successful
        ),
        "bridge_estimated_cost_usd": round(
            sum(receipt["response"]["estimated_cost_usd"] for receipt in successful), 10
        ),
        "models": sorted({receipt["response"]["model"] for receipt in successful}),
        "revision": {
            "patterns": sorted(revised_ids),
            "new_fixture_ids": sorted(added_fixture_ids),
            "preserved_superseded_fixture_ids": sorted(
                fixture["id"] for fixture in fixtures
                if fixture["pattern_id"] in revised_ids
                and fixture["version"] != patterns[fixture["pattern_id"]]["version"]
            ),
        },
        "scope": (
            "Synthetic author-labeled screens with immutable version history; not held-out "
            "accuracy, calibration, safety policy, or operational qualification."
        ),
    }


def run():
    result = report()
    print(json.dumps(result, indent=2))
    if result != read("results/summary.json"):
        raise SystemExit("saved summary differs from replay; preserve original disagreements")


if __name__ == "__main__":
    run()

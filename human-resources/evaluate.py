"""Replay Human Resources v1 history and version-bound current receipts offline."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "scripts"))
from collection_tools import replay as replay_collection, unique, validate_receipt  # noqa: E402


def read(path):
    """Read a JSON file relative to this collection."""
    return json.loads((ROOT / path).read_text())


def validate_fixture_history(old_fixtures, fixtures, old_patterns, patterns):
    """Preserve all original fixture content while allowing additive revisions."""
    before, after = unique(old_fixtures, "id"), unique(fixtures, "id")
    old_pattern_map, pattern_map = unique(old_patterns, "id"), unique(patterns, "id")
    if set(before) - set(after):
        raise ValueError("frozen fixture removed")
    if set(old_pattern_map) != set(pattern_map):
        raise ValueError("pattern inventory changed")
    for pid, pattern in pattern_map.items():
        old_pattern = old_pattern_map[pid]
        if type(old_pattern.get("version")) is not int or type(pattern.get("version")) is not int:
            raise ValueError("invalid pattern version")
        if pattern["version"] < old_pattern["version"]:
            raise ValueError("pattern version downgraded")
        if pattern["version"] > old_pattern["version"] + 1:
            raise ValueError("pattern version skipped")
        if pattern["version"] == old_pattern["version"]:
            old_content = {k: v for k, v in old_pattern.items() if k != "version"}
            current_content = {k: v for k, v in pattern.items() if k != "version"}
            if old_content != current_content:
                raise ValueError("contract changed without version increment")
    for fid, original in before.items():
        current = after[fid]
        old_content = {k: v for k, v in original.items() if k != "version"}
        current_content = {k: v for k, v in current.items() if k != "version"}
        if old_content != current_content:
            raise ValueError("frozen fixture was rewritten")
    for fid, fixture in after.items():
        fixture_version = fixture.get("version")
        if type(fixture_version) is not int or fixture_version < 1:
            raise ValueError("invalid fixture version")
        pattern = pattern_map.get(fixture["pattern_id"])
        if pattern is None or fixture_version != pattern["version"]:
            raise ValueError("fixture version does not match current contract")
        if fid not in before:
            old_pattern = old_pattern_map.get(fixture["pattern_id"])
            if old_pattern is None or pattern["version"] <= old_pattern["version"]:
                raise ValueError("new fixture must target a revised contract")


def report():
    catalog, fixtures, sources = read("catalog.json"), read("fixtures.json"), read("sources.json")
    initial_catalog = read("results/initial-catalog.json")
    initial_fixtures = read("results/initial-fixtures.json")
    initial_sources = read("results/initial-sources.json")
    initial = read("results/screening.json")
    refinement = read("results/refinement.json")
    validate_fixture_history(
        initial_fixtures, fixtures, initial_catalog["patterns"], catalog["patterns"],
    )

    old_patterns = unique(initial_catalog["patterns"], "id")
    current_patterns = unique(catalog["patterns"], "id")
    revised_ids = {
        pid for pid, pattern in current_patterns.items()
        if pattern["version"] > old_patterns[pid]["version"]
    }
    if not revised_ids:
        raise ValueError("no versioned refinements found")
    initial_result = replay_collection(
        initial_catalog, initial_fixtures, initial_sources, initial, [],
    )
    revised_catalog = {
        "title": catalog["title"],
        "patterns": [p for p in catalog["patterns"] if p["id"] in revised_ids],
    }
    revised_fixtures = [f for f in fixtures if f["pattern_id"] in revised_ids]
    refinement_result = replay_collection(
        revised_catalog, revised_fixtures, sources, refinement, [],
    )
    selected = [r for r in initial if r["pattern_id"] not in revised_ids] + refinement
    current_result = replay_collection(catalog, fixtures, sources, selected, [])

    fixture_map = unique(fixtures, "id")
    pattern_map = unique(catalog["patterns"], "id")
    selected_map = unique(selected, "fixture_id")
    review_required = []
    for fixture in fixtures:
        receipt = selected_map[fixture["id"]]
        if not receipt["response"].get("ok"):
            continue
        answer = receipt["response"]["answers"]["decision"]
        threshold = pattern_map[fixture["pattern_id"]]["policy"]["review_when_confidence_below"]
        if answer["confidence"] < threshold:
            review_required.append({
                "fixture_id": fixture["id"],
                "pattern_id": fixture["pattern_id"],
                "expected": fixture_map[fixture["id"]]["expected"],
                "observed": answer["choice"],
                "confidence": answer["confidence"],
                "review_below": threshold,
            })

    all_successful = [
        r for r in [*initial, *refinement] if r["response"].get("ok") is True
    ]
    result = dict(current_result)
    result["initial"] = initial_result
    result["refinement"] = refinement_result
    result["request_digests_verified"] = len(all_successful)
    result["recorded_provider_input_tokens"] = sum(
        r["response"]["usage"]["input_tokens"] for r in all_successful
    )
    result["recorded_provider_output_tokens"] = sum(
        r["response"]["usage"]["output_tokens"] for r in all_successful
    )
    result["recorded_bridge_estimated_cost_usd"] = round(
        sum(r["response"]["estimated_cost_usd"] for r in all_successful), 10
    )
    result["review_required"] = review_required
    result["revision"] = {
        "patterns": sorted(revised_ids),
        "new_fixture_ids": sorted(
            f["id"] for f in fixtures if f["id"] not in {x["id"] for x in initial_fixtures}
        ),
        "selected_current_receipts": len(selected),
        "preserved_initial_receipts": len(initial),
        "versioned_refinement_receipts": len(refinement),
    }
    return result


if __name__ == "__main__":
    result = report()
    print(json.dumps(result, indent=2))
    if result != read("results/summary.json"):
        raise SystemExit("saved summary differs from replay")

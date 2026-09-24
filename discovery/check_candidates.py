"""Check the discovery candidate registry; no network, inference, or novelty claim."""
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
STATUSES = {"candidate", "experimental", "folded", "reclassified", "rejected", "promoted"}
CLOSED = {"folded", "reclassified", "rejected", "promoted"}
TEXT_FIELDS = ("title", "mechanism", "jev_judges", "code_owns", "delta", "next_step")
FOUNDATIONS = {"evidence-directed-allowlist-controller", "lineage-aware-corroboration",
               "dependency-dag-selective-recomputation"}
# Tripwires for private material copied from live work; not a privacy guarantee.
PRIVATE = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "email address"),
           (re.compile(r"\b\d{9,}\b"), "long digit sequence"),
           (re.compile(r"\b(?:sk|pk|api|key|token)[-_][A-Za-z0-9]{12,}", re.I), "credential-like token")]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def prior_ids(repo=REPO):
    ids = set(FOUNDATIONS)
    catalogs = sorted(repo.glob("iterations/[0-9][0-9]/catalog.json"))
    catalogs += [m.with_name("catalog.json") for m in sorted(repo.glob("*/collection.json")) if m.with_name("catalog.json").exists()]
    for path in catalogs + [repo / name for name in ("email/catalog.json", "bug-hunting/catalog.json",
                                                     "human-ai/catalog.json")]:
        ids.update(p["id"] for p in json.loads(path.read_text())["patterns"])
    return ids


def validate(registry, known, repo=REPO):
    require(registry.get("schema_version") == 1, "schema_version must be 1")
    require(set(registry.get("statuses", {})) == STATUSES, "status definitions mismatch")
    candidates = registry.get("candidates")
    require(isinstance(candidates, list) and candidates, "candidates required")
    numbers, titles, counts = [], set(), {}
    for c in candidates:
        cid = c.get("id", "")
        require(isinstance(cid, str) and re.fullmatch(r"C[1-9][0-9]*", cid), "bad id: " + repr(cid))
        numbers.append(int(cid[1:]))
        for field in TEXT_FIELDS:
            require(text(c.get(field)), cid + " needs " + field)
        title = c["title"].strip().lower()
        require(title not in titles, cid + " repeats a title")
        titles.add(title)
        require(c.get("status") in STATUSES, cid + " has unknown status")
        counts[c["status"]] = counts.get(c["status"], 0) + 1
        require(text(c.get("resolution")) == (c["status"] in CLOSED),
                cid + " needs resolution exactly when closed")
        found = c.get("found") or {}
        require(all(text(found.get(k)) for k in ("date", "harness", "context")), cid + " needs found date/harness/context")
        date.fromisoformat(found["date"])
        prior = c.get("nearest_prior")
        require(isinstance(prior, list) and prior, cid + " needs nearest_prior")
        unknown = [p for p in prior if p not in known]
        require(not unknown, cid + " cites unknown prior patterns: " + ", ".join(map(str, unknown)))
        evidence = c.get("evidence")
        require(isinstance(evidence, list) and evidence and all(text(e) for e in evidence), cid + " needs evidence")
        for item in evidence:
            if "/" in item and " " not in item and "://" not in item:
                require((repo / item).exists(), cid + " evidence path missing: " + item)
            for pattern, label in PRIVATE:
                require(not pattern.search(item), cid + " evidence contains " + label)
        for field in TEXT_FIELDS + ("resolution",):
            for pattern, label in PRIVATE:
                require(not pattern.search(c.get(field) or ""), cid + " " + field + " contains " + label)
        for pattern, label in PRIVATE:
            require(not pattern.search(found["context"]), cid + " context contains " + label)
    require(numbers == sorted(numbers) and len(set(numbers)) == len(numbers), "ids must be unique and ascending")
    return {"candidates": len(candidates), "by_status": dict(sorted(counts.items())),
            "next_id": "C" + str(max(numbers) + 1),
            "scope": "Structural registry check; not screening, novelty, or privacy certification."}


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "candidates.json"
    print(json.dumps(validate(json.loads(path.read_text()), prior_ids()), indent=2))

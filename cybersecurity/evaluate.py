"""Replay this collection's synthetic screening receipts; no network or model calls."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "scripts"))
from collection_tools import digest, replay, run, validate_collection, validate_receipt  # noqa: E402,F401


def read(path):
    """Read a JSON file relative to this collection."""
    return json.loads((ROOT / path).read_text())


if __name__ == "__main__":
    run(ROOT)

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "historical_measure", Path(__file__).parent / "introduction-review/measure.py")
measure = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(measure)


class HistoricalMeasurements(unittest.TestCase):
    def test_saved_report_replays_all_pins_and_five_frozen_inputs(self):
        saved = json.loads(measure.SAVED.read_bytes())
        self.assertEqual(len(saved["input_files"]), 25)
        historical = {"email/results/refinement.json",
                      *(f"iterations/{i:02d}/catalog.json" for i in range(1, 5))}
        frozen = {p.stem: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (measure.ROOT / "frozen-inputs").glob("*.json")}
        self.assertEqual(frozen, {saved["input_files"][n]: saved["input_files"][n] for n in historical})
        self.assertEqual(measure.report(), saved)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.review = self.repo / "review"
        self.review.mkdir()
        self.saved = self.review / "measurements.json"
        self.name = "iterations/03/catalog.json"
        self.live = self.repo / self.name
        self.live.parent.mkdir(parents=True)

    def test_new_baseline_hashes_live_bytes_and_can_be_replayed(self):
        old = b'{"edition": "archived"}'
        new = b'{"edition": "live"}\n'
        digest = hashlib.sha256(old).hexdigest()
        frozen = self.review / "frozen-inputs" / (digest + ".json")
        frozen.parent.mkdir()
        frozen.write_bytes(old)
        self.live.write_bytes(new)
        with patch.multiple(measure, REPO=self.repo, ROOT=self.review, SAVED=self.saved,
                            RECEIPT_DIRS=[self.repo / "iterations"]):
            docs, hashes = measure.load_all()
            self.assertEqual(docs, [(self.name, json.loads(new))])
            self.assertEqual(hashes, {self.name: hashlib.sha256(new).hexdigest()})
            self.saved.write_text(json.dumps({"input_files": hashes}))
            self.assertEqual(measure.load_all(), (docs, hashes))
            self.saved.write_text(json.dumps({"input_files": {self.name: digest}}))
            self.assertEqual(measure.load_all()[0], [(self.name, json.loads(old))])
            self.assertEqual(self.live.read_bytes(), new)

    def test_corrupt_or_missing_frozen_input_fails_closed_on_drift(self):
        digest = hashlib.sha256(b'{"edition": "original"}').hexdigest()
        self.live.write_text('{"edition": "different"}')
        self.saved.write_text(json.dumps({"input_files": {self.name: digest}}))
        with patch.multiple(measure, REPO=self.repo, ROOT=self.review, SAVED=self.saved):
            with self.assertRaisesRegex(SystemExit, "pinned input changed"):
                measure.load_all()
            frozen = self.review / "frozen-inputs" / (digest + ".json")
            frozen.parent.mkdir()
            frozen.write_bytes(self.live.read_bytes())
            self.live.write_bytes(b'{"edition": "original"}')
            with self.assertRaisesRegex(SystemExit, "pinned input changed"):
                measure.load_all()

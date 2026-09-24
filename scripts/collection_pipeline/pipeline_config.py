"""Shared locations for the collection pipeline.

REPO is this repository. WORKDIR holds authoring drafts, challenge cases, and browser
page records (default <repo>/.work, git-ignored; override with JEV_PATTERNS_WORKDIR).
CLI is the local jev-workflows bridge that reads the API key from the macOS Keychain
(override with JEV_WORKFLOWS_CLI). Nothing here embeds a credential.
"""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WORKDIR = Path(os.environ.get("JEV_PATTERNS_WORKDIR", REPO / ".work"))
CLI = os.environ.get("JEV_WORKFLOWS_CLI", str(Path.home() / "Code/jev-workflows/.venv/bin/jev-workflows"))
WORKDIR.mkdir(parents=True, exist_ok=True)

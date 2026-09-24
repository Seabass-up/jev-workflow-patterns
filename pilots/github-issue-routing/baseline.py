"""Frozen deterministic comparison, operating only on an issue title."""

import re

BUG_CUES = re.compile(
    r"crash|panic|fail|error|bug|broken|incorrect|wrong|ignore|missing|"
    r"doesn't|does not|cannot|can't|unable|not found|empty|silently|unexpected|"
    r"lose|throttle|flash|still requires",
    re.IGNORECASE,
)
FEATURE_START = re.compile(
    r"^(add|allow|support|enable|make|update|show|tell|ability)\b",
    re.IGNORECASE,
)


def decide(title):
    if BUG_CUES.search(title):
        return "bug_queue"
    if FEATURE_START.search(title):
        return "enhancement_queue"
    return "human_review"

# Iteration 3: Jev question contracts

Thirty public, synthetic-screened typed-question patterns:

- 7 business patterns (B15–B21)
- 7 engineering patterns (E15–E21)
- 6 LLM components (L13–L18)
- 10 harness compositions (H21–H30)

The machine-readable catalog.json is the canonical contract source. fixtures.json
contains frozen synthetic expected labels outside submitted state. The results directory
retains the initial raw screen, targeted refinement, source selection, duplicate comparison,
and final acceptance selection. evaluate.py verifies receipt integrity with no provider call.

This is a public design/evaluation artifact, not a production runtime, calibration study,
or authority to perform external actions.

## Local contract review — 2026-09-26

L17 is version 3 after a documented v2 incomplete-description miss; L18 and H28 are
version 2 with explicit task-depth and fan-out precedence. The v2 miss, bounded v3
re-screen, option-pair judgments, and side-effect-free consumer checks are retained in
the evaluation artifacts. Current selected synthetic receipts replay 73/73 fixtures and
98/98 question checks. This is regression evidence only, not production qualification;
one H24 availability boundary remains conservatively review-held.

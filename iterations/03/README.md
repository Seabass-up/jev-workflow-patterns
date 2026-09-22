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

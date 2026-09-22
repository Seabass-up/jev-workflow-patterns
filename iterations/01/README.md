# Iteration 1: 30 Jev question patterns

20 core patterns (7 business, 7 engineering, 6 LLM) plus 10 experimental harness compositions. Synthetic screening only; no production or global novelty claim.

- Read the [public catalog](https://seabass-up.github.io/jev-workflow-patterns/iterations/01/).
- Review [evaluation.md](evaluation.md), including preserved failures.
- Use `catalog.json` for current questions; `screens.json` preserves the exact question versions and synthetic fixtures used in each screen.
- `results/` contains full synthetic Jev replies, uncertainty, request digests and accounting.
- `evaluate.py` verifies receipts and supplies pure advisory controller examples. It does not perform operational actions.
- `test_evaluate.py` contains 31 offline tests. No third-party packages or provider key are needed for offline replay.

## Offline reproduction

From this directory:

```sh
python3 evaluate.py
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The replay recomputes 136 request hashes and label/range comparisons. Known model mismatches are reported as evidence; they are not erased to make the test suite green.

## Optional single-fixture live replay

Install and configure your own approved Jev bridge first; credentials must remain server-side or in your existing secure credential store. This repository does not ship the bridge or handle keys. The explicit live option makes one request, not a batch:

```sh
python3 evaluate.py --live --screen core-refinement --fixture B02-new-1 --bridge /path/to/configured/jev-workflows
```

The command sends only synthetic state and questions to TypeSafe, disables caching and prints a fresh receipt to stdout. Expected labels remain local. The bridge owns its model configuration, deadline and credentials; a replay may use a different model unless you pin it. Do not overwrite historical receipts with a fresh response.

## Evidence boundary

Original screen: 76/81 fixtures. Targeted follow-up: 15/15, comprising 8 reused and 7 fresh diagnostic cases. Harness components: 38/40. H01 is held for grounding redesign after two high-probability incorrect plausibility answers. Controllers are illustrations, not a supported SDK, authorization system or production integration. See the parent repository's ownership/license notice.

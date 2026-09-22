# Jev Workflow Patterns — Iteration 2

This directory is the second public catalog iteration for bounded Jev question
contracts. It publishes 30 patterns across business, engineering, LLM workflow,
and experimental harness domains.

It deliberately contains synthetic state only. No API key, local Keychain bridge,
private corpus, production integration, or authority to execute actions is part of
this directory.

## What was tested

- Final catalog: 30 patterns
- Final fixtures: 134
- Final question checks: 147
- Saved live synthetic receipts: 168
- Final selected latest-contract receipts: 134/134 fixture matches and 147/147 question checks

That final match rate is a regression result after iterations on the same
synthetic set. It is not an accuracy, calibration, or production-readiness claim.

## Reproduce offline verification

~~~text
python3 evaluate.py
python3 -m unittest -v test_evaluate.py
~~~

The verifier checks typed answer shape, exact request digests, label isolation
from submitted state, receipt coverage, and the final-contract receipt mapping.
It performs no network request unless an operator explicitly uses
the --live option with one synthetic fixture.

## Start here

- [Public catalog page](https://seabass-up.github.io/jev-workflow-patterns/iterations/02/)
- [Question kernel](question-kernel.md)
- [Evaluation details](evaluation.md)
- [Sources and research boundaries](sources.md)
- [Machine-readable catalog](catalog.json)
- [Final fixtures](fixtures.json)

---
layout: default
title: "Iteration 3 Evaluation"
description: "Preserved synthetic Jev receipts, question revisions, fixture correction, and offline integrity checks."
permalink: /iterations/03/evaluation/
kicker: "Evaluation · frozen fixtures and versioned contract repair"
---

[← Iteration 3 catalog]({{ '/iterations/03/' | relative_url }}) · [Question kernel]({{ '/iterations/03/question-kernel/' | relative_url }}) · [Raw summary]({{ '/iterations/03/results/summary.json' | relative_url }})

# Evaluation: preserve the initial miss, repair only the demonstrated boundary

This is a small synthetic contract screen. It asks whether deliberately clear,
synthetic states produce the intended typed answer under the exact question contract.
It does not measure production accuracy, calibration, security, legal compliance,
real-world authority, or global novelty.

## Result timeline

| Stage | Requests | Fixture matches | Question checks | What happened |
| --- | ---: | ---: | ---: | --- |
| Initial frozen v1 screen | 61 | 58 / 61 | 81 / 84 | Three semantic/fixture boundaries missed; all raw receipts remain public. |
| Targeted refinement | 6 | 6 / 6 | 17 / 17 | E16 and L14 were versioned; one H24 fixture was clarified and rerun. |
| Final selected contracts | 61 | 61 / 61 | 84 / 84 | The latest matching receipt for every current fixture/contract is selected. |

The 67 live synthetic calls used 33,989 billed input tokens, 4,281 output tokens, and
an estimated provider cost of $0.001427538. Those are observed historical receipts, not
a price quote or a claim about a production workload.

## Initial misses and repairs

| Pattern / fixture | Initial observation | Repair and evidence boundary |
| --- | --- | --- |
| E16 configuration conflict | The v1 wording returned insufficient when the state gave incompatible values and said both must control without a resolution. | Contract v2 explicitly classifies that stated condition as explicit_conflict; both E16 fixtures were rerun. |
| L14 neutral question | A neutral “does the policy permit” query received a high premise-conflict Noul despite no affirmative premise. | Contract v2 explicitly says a neutral question does not assert permission/truth/availability; all three L14 fixtures were rerun. |
| H24 limited-fit veto fixture | A “limited fit” synthetic state received score 0.63, just outside its author-assigned 0–0.6 bin. | The fixture now states no fit, which is the intended low-score boundary. The original receipt remains intact and the clarified state was rerun under the unchanged H24 v1 contract. |

Making a final synthetic regression set perfect after inspecting misses does not establish
generalization. Production use needs independently adjudicated, representative data,
predeclared consequence policy, and calibration against the target workflow.

## Receipt integrity

The offline evaluator verifies:

- response shapes match the exact Choice, Score, or Noul question contract;
- every request digest binds model, synthetic state, and question JSON;
- expected labels never enter submitted state;
- stored observed values and match flags recompute from raw typed output;
- every final fixture is linked to the current contract version and exact current state;
- pure controllers return review, calculation, expansion, or verification proposals only.

Run locally:

~~~text
python3 iterations/03/evaluate.py
python3 -m unittest discover -s iterations/03 -p 'test_*.py' -v
~~~

[Initial raw receipts]({{ '/iterations/03/results/initial-screen.json' | relative_url }}) · [Refinement raw receipts]({{ '/iterations/03/results/refinement-screen.json' | relative_url }}) · [Final receipt selection]({{ '/iterations/03/results/final-acceptance.json' | relative_url }}) · [Offline evaluator]({{ '/iterations/03/evaluate.py' | relative_url }})

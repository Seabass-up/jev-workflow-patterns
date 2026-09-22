# Evidence and provenance

Use this module when the result depends on a specific source, extracted field,
quotation, association, or claimed causal relationship.

## Preflight in code

Resolve sources through the authorized retrieval path. Bind identity, revision, and
location to the actual bytes used. A digest binds bytes but cannot prove authenticity,
completeness, or independence. Recheck relevant freshness after state changes.

For quotations, perform exact lookup using a declared comparison policy. Preserve
original text and offsets when normalization is used. If lookup fails, return
`quote_missing` or retrieve the missing source; skip semantic support inference.
For candidate selection, validate membership and copy the selected source value
with code. Do not generate replacement values.

## Semantic checks to select

| Evidence relation | Question to adapt | Patterns |
| --- | --- | --- |
| Field and source | Does the evidence support this field in the intended record? | E22, H33 |
| Labels and values | Are the values associated with the correct labels? | E23 |
| Located quote and claim | Does the surrounding context support the claim? | H37 |
| Trace events | Is causality evidenced, or only request identity/time correlation? | E25 |
| Parsed candidate | Which supplied span expresses the requested value? | H34 |
| Feature evaluation | Are feature revision, held-out split, and metric evidence bound? | H38 |

Provide surrounding context and explicit insufficient/conflict criteria. Batch
independent fields and consume only applicable results. Retain contradictions.
For feature metrics, code determines direction, differences, and split membership.
Jev can assess methodology text; it cannot prove that the evaluation actually ran.

## Report and consume

Keep source references, exact checks, semantic answers and probabilities, unresolved
gaps, and the caller's next step distinct. Preserve original judgments after escalation.
Quotation support does not authorize publication; stated role evidence does not
authorize disclosure. Apply the task's actual permissions at the point of action.

Select checks based on the real relation. A sentiment classifier may need no quote
or trace analysis. Find the exact pattern via [profiles.md](profiles.md).

Official references: [citations](https://docs.typesafe.ai/cookbooks/citation_check),
[extraction cascade](https://docs.typesafe.ai/cookbooks/sde_cascade), and
[candidate extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook).

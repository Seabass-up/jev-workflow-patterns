# Call-control profiles

Use this module for the code around a Jev call: preparing a request, consuming an
answer, checking a contract before inference, and reading message signals. The
object of judgment is supplied text; thresholds, identities, equality, execution,
and verification stay in code.

## Select the control that fits

The [10 profiles](https://seabass-up.github.io/jev-workflow-patterns/controls/)
are optional examples, not a checklist for every call:

| IDs | Family | Useful checks |
| --- | --- | --- |
| CT03, CT04, CT05 | Preparing the request | Compound-request detection, split coverage, translation fidelity for a stated purpose |
| CT01, CT02 | Consuming the answer | Runner-up consumer outcome, free-text argument target |
| CT06, CT07, CT08 | Contract quality | Labeler rationale agreement, negation-pair validity, option overlap |
| CT09, CT10 | Message signals | Credential request versus self-service reset, link text versus parsed host |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/controls/patterns/<lowercase-id>/`
and the versioned contracts are in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/controls/catalog.json).
CT03, CT07, and their evaluation retain disagreements; read the
[evaluation](https://seabass-up.github.io/jev-workflow-patterns/controls/evaluation/)
before adapting a provisional profile.

Choose between nearby controls by what code already knows:

- CT01 applies only when handler effects are described in prose. When labels map to
  handlers in code, sum probabilities per handler in code and ask nothing.
- CT02 takes one free-text parameter per question. Enumerated, numeric, identifier,
  and schema checks belong in code before any question is asked.
- CT04 decides whether to split; CT03 checks a split the language model produced.
  Cap the number of commands and require confirmation before multi-action execution.
- CT08 runs before fixtures are frozen. This collection ran it over its own option
  pairs and over two sibling collections; the record is in
  `controls/results/overlap-review.json`.

## Record thresholds with their option count

Choice confidence closely follows `(n × top probability − 1) / (n − 1)`. Every
profile here records `review_when_confidence_below` together with `option_count`
and the equivalent top probability. Re-tune when an option is added or removed, and
use `scripts/check_confidence.py` to convert or to verify stored receipts. Runner-up
mass matters only when the runner-up would lead somewhere else; CT01 exists for that.

## Prepare a bounded state

Bind the exact request, tool description, handler descriptions, contract text, or
message under judgment, with its revision. For CT09 and CT10, code supplies the
credential list and the organization-to-host registry; the model never parses a URL
or decides policy. Before inference, code validates `required_state_fields` and
returns a local `unknown` for absent or empty required evidence. Three missing-input
probes in this screen were classified instead of returning unknown, which is why
that gate is code's job, not the model's.

## Use the labels without taking over

A label prepares or filters; it never executes. `disclose_credential` feeds a
code-owned veto. `adds_an_action` or `drops_an_action` sends the request back for one
re-split, then to the person. `meaning_changed` fails the translate-then-ask path
closed. `different_reading` removes an item from agreed labels; it does not call
another model. CT07's screen preserved a case where a non-complement pair was
labelled a complement: treat that probe as experimental and keep it at design time.

## Verify in the consuming workflow

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/controls/evaluation/)
separates 30 design cases from 10 separately authored challenge cases. Before use,
replay recorded traces, splits, translations, or messages with known defects, measure
detection and false alarms per defect type, and keep the deterministic gates outside
the model. Synthetic agreement is not qualification.

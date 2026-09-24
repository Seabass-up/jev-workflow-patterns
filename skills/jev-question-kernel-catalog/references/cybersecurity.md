# Cybersecurity operations profiles

Use this module for classifying the text a security operations analyst handles:
user-reported emails, alert narratives with their stated context, vulnerability
advisories against asset descriptions, incident reports against a severity
definition, access and policy-exception requests, single log events, and vendor
questionnaire answers. A label is a reading of text. Indicator, hash, address, and
version matching, thresholds, containment, and every access decision stay with
code and people, and nothing in these profiles describes attack techniques or
tooling.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/cybersecurity/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| CY01, CY02, CY04, CY07 | Triage | The ask a reported email makes; stated context against an alert narrative; a report against a severity definition; the authentication outcome one log event describes |
| CY05, CY06, CY08 | Requests and reviews | Task-bound access justification; compensating control in an exception request; vendor answer responsive to the question |
| CY03 | Advisories | Advisory names the product or an included component of a described asset |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/cybersecurity/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/cybersecurity/catalog.json).
The evaluation page reports screening outcomes; those are small synthetic checks,
not qualification for a real operations team.

Choose by what the label feeds:

- CY01 feeds the report queue. It names the ask a message makes, never whether the
  sender is genuine; sender domains, link hosts, and attachment hashes are checked in
  code, and quarantine, blocking, and notifying finance are analyst actions. The
  controls profile CT09 is the narrower credential-disclosure check when a
  credential-term list is available.
- CY02 and CY04 feed the analyst's disposition and the incident lead's severity
  call. CY02 says which described signs a stated explanation leaves unexplained and
  never whether the explanation is true; CY04 reads a supplied definition as data and
  leaves numeric thresholds to code.
- CY03 filters the advisory feed before code compares versions, builds, and patch
  levels exactly. A `same_product_named` label schedules a comparison, not a patch.
- CY05 and CY06 feed the approver and the risk owner. Neither label grants access or
  an exception, and adequacy of a compensating control is the risk owner's judgment.
- CY07 normalizes one event's wording. Code parses identifiers, counts events, applies
  lockout and alerting thresholds, and takes any account action.
- CY08 points reviewer time at vendor answers that need follow-up; the adequacy of
  a described practice stays with the reviewer.

## Prepare a bounded state

Supply the reported message, alert narrative, advisory text, report, request, log
event, or answer unchanged, together with the definition, requirement, asset
description, or question it is judged against, as code holds them. Supply one log
event per CY07 call and one question-answer pair per CY08 call. Several contracts
state a precedence order for text that satisfies more than one label (a message
making two asks, a lockout that also records a failure, an answer that both
declines and answers part); those sentences were added after a pre-inference overlap
check, so keep them when adapting. Before inference, code validates
`required_state_fields` and returns a local `unknown` for absent or empty evidence.

## Use the labels without taking over

No label declares a message malicious or safe, closes an alert, assigns a severity,
grants access or an exception, rates a vendor, or triggers containment. Send only
authorized operational text through the approved provider path; keep account
credentials, one-time codes, full addresses, hashes, customer identities, and case
identifiers out of the state unless the judgment needs them and the transfer is
authorized. Redact reported messages of any secret a user pasted before they enter
the state.

## Verify against the team's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/cybersecurity/evaluation/)
reports outcomes for the design cases and any separately authored challenge cases.
Before use, compare labels with analyst dispositions on reported messages and
alerts, the severity the incident lead assigned, approver and risk-owner decisions,
parser-labeled authentication events per log source, and reviewer follow-ups on
completed questionnaires. Measure first the payment-change and sign-in asks filed
as `none_of_these`, the alerts labeled `fully_accounted_for` that were later true
positives, and the lockouts labeled as no authentication outcome.

# Logistics profiles

Use this module for classifying the text a logistics coordinator and a warehouse system
handle: carrier exception updates, proof-of-delivery notes, inbound customs documents,
receiving notes, claim narratives, order notes, supplier messages about open orders, and
notes explaining a missed delivery commitment. A label is a reading of text. Quantities,
dates, amounts, carrier terms, claim liability, and customs declarations stay with code
and people. A sibling collection covers routing; this one stays on shipments and documents.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/logistics/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| LG01, LG02, LG08 | Carrier updates and delivery | Exception type in a tracking update; who, if anyone, accepted a delivery; stated cause of a missed commitment |
| LG03, LG04, LG05, LG06 | Documents, receiving, and claims | Customs document type; receiving discrepancy type; stated cause of damage in a claim; handling or delivery instruction in an order note |
| LG07 | Supplier messages | Backorder, substitution, or cancellation in a supplier message |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/logistics/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/logistics/catalog.json).
The evaluation page reports screening outcomes; a small synthetic check is not
qualification for a real operation.

Choose by what the label feeds:

- LG01 feeds the exception queue. Code matches the tracking identifier, compares scan
  times with promised dates, and opens a trace or claim under the carrier's rules.
- LG02 answers where a package went. The carrier's timestamp, location, and signature
  record remain the evidence; the label never establishes that the addressee has the goods.
- LG03 files a customs document by type. Code validates fields, values, and tariff codes,
  and the broker owns the declaration.
- LG04 and LG05 code receiving and claim text. Code compares received and expected
  quantities, posts adjustments, and records claim amounts and deadlines; people decide
  liability and chargebacks.
- LG06 flags an order note for the packer or the carrier booking. Code decides which
  instructions the service level allows.
- LG07 routes a supplier message. The purchase order changes only after a buyer accepts
  a substitution, and dates are compared in code.
- LG08 groups missed commitments by stated cause for reporting. Code decides from
  timestamps whether a commitment was missed and applies any credit or penalty terms.

## Prepare a bounded state

Supply the carrier's, driver's, receiver's, claimant's, or supplier's words unchanged,
one message or note per call. Do not add expected quantities, promised dates, or claim
amounts for the model to compare; keep those in code and let the note say in words what
the writer observed. Several contracts state a precedence order for text that reports
more than one problem, cause, or announcement (LG01, LG02, LG04, LG05, LG06, LG07, LG08);
keep those sentences when adapting. Before inference, code validates
`required_state_fields` and returns a local `unknown` for absent or empty evidence.

## Use the labels without taking over

No label decides a claim, assigns liability, computes a shortage, resolves a delivery
date, applies a service credit, or classifies goods for customs. Send only authorized
shipment text through the approved provider path; keep customer names, addresses,
tracking numbers, account numbers, and signature images out of the state unless the
judgment needs them and the transfer is authorized. Proof-of-delivery and claim labels
are readings of what a note asserts, not findings about what happened.

## Verify against the operation's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/logistics/evaluation/)
page reports how the design cases and any separately authored challenge cases fared.
Before use, compare labels with coordinator tags on carrier updates, dispute outcomes on
deliveries, discrepancy codes receivers entered by hand, the cause a claims adjuster
recorded after review, buyer actions on supplier messages, and the analyst's cause codes
on service failures. Measure first the handed_to_recipient labels that later became
not-received claims and the matches_expected labels that later needed an adjustment.

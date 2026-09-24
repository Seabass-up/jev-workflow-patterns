# Logistics routing profiles

Use this module for classifying the text a dispatch desk and routing software read:
address notes, delivery-window requests, stop instructions, driver reports, reschedule
messages, order text, multi-stop requests, and address text. A label is a reading of
text. Distance, time, capacity, and sequencing are computed in code, and the model
never chooses a route. Shipment documents and freight paperwork are not this
module's subject.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/logistics-routing/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| LR01, LR03, LR06, LR08 | Stops and addresses | Access constraint in an address note; kind of stop instruction; hazardous or temperature declaration in order text; how many places an address text names |
| LR02, LR05, LR07 | Windows and sequence | Kind of time constraint in a window request; whether a reschedule proposes a time or defers; ordering or grouping constraint across stops |
| LR04 | Driver reports | Cause a driver states for a route deviation |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/logistics-routing/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/logistics-routing/catalog.json).
The evaluation page reports screening outcomes; those are small synthetic checks,
not qualification for a real dispatch desk.

Choose by what the label feeds:

- LR01, LR03, and LR08 feed stop preparation. Code stores gate codes and contact
  details as exact strings, matches vehicle restrictions against fleet dimensions,
  and geocodes or asks the customer to choose when the text names several places.
- LR02 and LR05 feed the calendar. Code copies the verbatim time expression, resolves
  it against the calendar and time zone, and checks route capacity; the model only
  says what kind of expression it is.
- LR07 feeds the routing solver as a precedence or same-route rule that code encodes
  and solves. The label never orders the stops.
- LR06 flags a declaration to reconcile with the product master, which owns the
  regulatory class and temperature band of record.
- LR04 tags the day's log. Telematics timestamps, not the label, measure the delay.

## Prepare a bounded state

Supply the customer's or driver's words unchanged, and for LR07 the stop list code has
already identified. Several contracts state a precedence order for text that mentions
more than one constraint, instruction, cause, or timing preference; those sentences
resolve overlaps found during authoring, so keep them when adapting. Before inference,
code validates `required_state_fields` and returns a local `unknown` for absent or
empty evidence.

## Use the labels without taking over

No label chooses a route, orders stops, resolves a date, assigns a vehicle, or
classifies goods for regulatory purposes. Send only authorized dispatch text through
the approved provider path; keep customer names, exact addresses, gate codes, and
contact details out of the state unless the judgment needs them and the transfer is
authorized.

## Verify against dispatch's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/logistics-routing/evaluation/)
separates design cases from separately authored challenge cases and reports the
outcomes. Before use, compare labels with the fields dispatchers filled in, the windows
customers later confirmed, the constraints planners entered, telematics for the same
trips, and the product master's flags. Measure missed vehicle restrictions and missed
hazard declarations first, since those change the assignment.

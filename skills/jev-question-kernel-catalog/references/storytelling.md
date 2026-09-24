# Storytelling profiles

Use this module for bounded checks of manuscript text against the author's own
context: a scene summary, a character's permitted knowledge, a story-bible entry, a
voice profile, a planted setup, or what the reader has been told. The object of
judgment is the supplied passage, never the author's ability, and every revision
decision stays with the author.

## Select the check that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/storytelling/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| ST01, ST06 | Structure | Scene changes the situation; a later passage pays off a setup |
| ST02, ST03, ST08 | Consistency | Viewpoint kept; story-bible contradiction; reader grounding |
| ST04, ST05, ST07 | Craft | Emotion stated or rendered; speaker attribution; voice profile |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/storytelling/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/storytelling/catalog.json).
ST04, ST05, and ST08 retain disagreements; read the
[evaluation](https://seabass-up.github.io/jev-workflow-patterns/storytelling/evaluation/)
before adapting them.

Choose between nearby checks by the context code can supply:

- ST02 needs a per-character knowledge ledger; ST08 needs a reader-knowledge ledger
  built from the manuscript order. Both ledgers are code's, updated after each passage.
- ST03 takes one story-bible entry per question. Select the relevant entries in code.
- ST06 pairs one setup with one candidate payoff passage; a mention is not a payoff.
- ST04 reports how emotion is conveyed. Stated emotion is sometimes the right choice;
  present the label, not a verdict.

## Prepare a bounded state

Supply the exact passage, its scene boundaries, and the author's own summaries,
profiles, and ledgers with their revisions. Keep omniscient or multi-viewpoint
sections out of ST02. Before inference, code validates `required_state_fields` and
returns a local `unknown` for absent or empty evidence; an empty character name and
an empty reader-knowledge list were both classified in this screen instead of
returning unknown.

## Use the labels without taking over

A label is information for revision. It does not edit text, decide that a scene must
be cut, or judge the writer. Ambiguous speakers, told emotion, and unpaid setups can
be deliberate. Preserve the author's explicit choices and record which flagged items
they kept.

## Verify with readers, not with agreement

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/storytelling/evaluation/)
separates 24 design cases from 8 separately authored challenge cases of original
fiction. Before use, compare labels with an editor's markup or with readers'
attributions and confusion on a real chapter, and count flagged items the author
kept on purpose. Synthetic agreement does not establish usefulness to a writer.

---
layout: default
title: "Pattern discovery intake"
description: "How patterns found while using Jev in real work become candidates, and how candidates reach the catalog."
permalink: /discovery/
kicker: "Discovery · from working use to the catalog"
---

# Capture patterns found while using Jev

Using Jev in real work turns up question designs, compositions, failure modes, and
code/Jev boundaries that the catalogs do not cover yet. This intake records them as
candidates, so a good idea from one task is not lost before it can be tested.

[Candidate registry]({{ '/discovery/candidates.json' | relative_url }})
· [Introduction review: C1–C9]({{ '/discovery/introduction-review/' | relative_url }})
· [Jev Question Kernel]({{ '/kernel/' | relative_url }})

## Add a candidate

1. **Check it is new.** Compare the mechanism, not the title, with the kernel's
   domain profiles and the nearest catalog patterns. A renamed duplicate is not a
   candidate; improving an existing pattern is a revision to that pattern.
2. **Describe it without private material.** Use synthetic or public examples only:
   no client names, private records, mailbox content, account numbers, or credentials.
   Evidence may cite a receipt digest instead of its private payload.
3. **Add the next `C` number** to `discovery/candidates.json` with the title,
   mechanism, what Jev judges, what code owns, evidence, nearest prior patterns,
   the delta from them, and the next step.
4. **Run the checker:** `python3 discovery/check_candidates.py`. It checks structure,
   known prior-pattern IDs, evidence paths, closed-status resolutions, and a few
   private-material tripwires. It does not judge novelty or certify privacy.

## Move a candidate forward

| Status | Meaning |
| --- | --- |
| `candidate` | Open; needs a contract, frozen fixtures, and a live screen. |
| `experimental` | Open; its premise must be validated before a contract is written. |
| `folded` | Merged into an existing pattern or kernel guidance. |
| `reclassified` | Continues as a different kind of item, such as an email profile. |
| `rejected` | Duplicate or unhelpful, with the reason recorded. |
| `promoted` | Published in a catalog, named in `resolution`. |

Promotion follows the catalog cycle: author the contract with the kernel, freeze
fixtures and expectations outside provider inputs, screen live, preserve misses, and
version any repair. An advisory Jev duplicate screen helps, but the kernel's
[review of the first screen]({{ '/discovery/introduction-review/' | relative_url }})
found design defects to avoid: ask one question per candidate–pattern pair, point
options at description paths, and include an insufficient-description outcome.

Candidates carry no novelty, accuracy, or endorsement claim. Adding one never
authorizes a commit, a live screen, or a change to a published pattern.

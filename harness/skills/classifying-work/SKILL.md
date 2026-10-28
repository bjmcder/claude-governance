---
name: classifying-work
description: Drafts, for the human owner to adopt, the classification record of the work or its revision, with the consequence class, the credible consequence and reliance that set it, the row of STND.CLASS.1, the cost threshold, the profiles selected, and the fields of the ledger entry that would adopt it. The draft is text only, and no file or ledger entry is written.
disable-model-invocation: true
argument-hint: "[CSQ0-CSQ4]"
---

# Drafting a classification

The class that the human owner named, if any: $ARGUMENTS

## What the draft is

The draft is text in the conversation. It is not a record. The classification is adopted only by the human owner (GOV.24, GOV.50); an agent may draft it. Under the defaults, the adoption is a ledger transaction of the human owner (STND.DFLT.13), and STND.DFLT.5 bars an agent from appending an entry that names the human owner as actor. A project constitution places the classification in its Classification section (STND.PROJ.1).

The provisions below print with `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -B -m govharness show "${CLAUDE_PLUGIN_ROOT}/governance" ID`.

## What a classification holds

| Content | Provision |
| --- | --- |
| The class, set as the most severe of the table row the work meets, the class a selected profile requires, and CSQ0 where the human owner states a credible path to physical harm | STND.CLASS.1 |
| A test in doubt, counted as met | STND.CLASS.2 |
| The amount above which a loss is a cost for the CSQ1 consequence test | STND.CLASS.3 |
| For the project and each component given a less severe class: the class, the credible consequence and the reliance that set it, and the row whose test each meets | STND.CLASS.5 |
| Evidence that each component given a less severe class is isolated | STND.CLASS.6 |
| The values of the selector attributes of each adopted profile, and the profiles selected | GOV.24, STND.PROJ.1 |
| The proportionality judgment, which is the classification entry itself | GOV.11, STND.CLASS.20 |

## Facts that bear on the class

- A class attaches to the use of the work and moves toward CSQ0 as reliance or exposure grows (GOV.14). STND.CLASS.7 lists the events that call for a reassessment.
- What each class requires above the floor, and from which class, is the table of STND.CLASS.10. Review independence by class is STND.CLASS.18, and the audit interval STND.CLASS.19.
- Under the defaults, an entry of the human owner that records CSQ0 or CSQ1 makes the work assured (the term Assured work of STND.DFLT). For assured work, STND.DFLT.23 accepts only entries signed by the human owner and confirmed by a key that the signer register lists. The corpus of this plugin has no signer register.
- The classification record has no field for a class that the work is expected to reach later, and no provision reads one (STND.CLASS.5). A rationale may state it as information.

## Shape of the draft

```text
Classification of <the work>

Consequence class: <class>
Credible consequence: <what an error would cause, and to whom>
Reliance: <who relies on the outputs, and through what verification>
Row of STND.CLASS.1: <class>, by its <consequence test, reliance test, or both>
Cost threshold (STND.CLASS.3): <amount>
Profiles selected: <identifiers, with the selector values that select them>
Components given a less severe class: <none, or each with its class and its evidence of isolation>

Ledger entry that would adopt it, for the human owner:
  type: classify
  actor: <the human owner's name>
  role: The Human Owner
  authority: GOV.13, GOV.24, STND.DFLT.13
  rationale: <the classification above, as one paragraph>
```

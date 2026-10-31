# Cold review of the LVL0 draft (revision 1.9), round of 2026-10-31

Method: applied `apply_audit_lvl0_2026_10_31.py` to a scratch copy, diffed against `harness/governance`, read the amended text with GOV.5/6/9 in mind, then read `decisions.md` (round) and `findings.md`, then the standing process. I did not read the drafter's `lvl0/decisions.md`. `verify` (full, with logic) on the copy: ids, mnemonics, references, manifests, ledger, unpinned, templates, status, checked-by, onset, logic all PASS; one `g.18` warning (more than three modals in a provision), which the unamended corpus also prints once. Not traced to a provision here. Titles are unchanged in every amended provision.

Coverage of outcomes: every LVL0 outcome of the round (S1, S2, S3, R1, R3 LVL0 part, R5, R8, R9, B2, B3, B10, I1, I3, I4, I5) is carried. Nothing extra was found beyond the GOV.10 `cites` change (GOV.10 dropped from GOV.13 because the text no longer cites it; correct).

## Findings

### L1 (High) PRIME.8: cost authorized without any bound

Quote: "the direction authorizes the operating cost of each agent that carries out the work in a configuration that the human owner provisioned, including each agent directed within an authority traceable to the direction." and "Implicit expenditure other than an agent's own operating cost proceeds only on a rigorously and faithfully derived estimate".

Problem: the estimate requirement is removed for the agent's own cost, and the halt applies only to limits "that the human owner sets or the environment enforces". Where the owner sets none and the environment enforces none, nothing bounds the spend. QA.3's stopping rule bounds only effort or cost "without progress toward its definition of done", so spend with progress is unbounded. The delegation clause adds fan-out: GOV.18 leaves any numeric limit on agents directed to LVL3, and STND.CREW.13 relied on an authorized estimate or envelope, which no longer need exist. Before this draft such work halted for want of an authorized estimate (the PRIME.8 intent).

Scenario: owner says "fix the bug in foo.py" on a metered, post-paid account with no cap. The lead agent directs sixteen reviewers and retries for hours; each step shows progress, so QA.3 never fires; no owner limit exists, so PRIME.8 never halts. The draft's rationale ("spending stays bounded by the human owner's acts and never by an agent's judgment") is not true for this case, and its own residual-risk note concedes it.

Fix: bound by something the owner has implicitly accepted. Proposed addition after the authorization sentence: "Absent such a limit, the authorization covers only the operating cost that the effort estimate of GUARD.14 states for the unit of work, and work halts before the cost exceeds that estimate by more than the stated tolerance; where the cost is unmeasurable, the configuration that the direction names bounds it." If the custodian prefers no number, at minimum say the authorization covers "the agents that the direction names or that the unit of work needs at the least costly configuration (GUARD.14)" and put the unbounded residual in the packet as a High risk, not a footnote. Also see L2 for the class argument.

### L2 (Medium) Revision class "minor" rests on a claim that L1 shows false

Quote (rationale): "spending stays bounded by the human owner's acts and never by an agent's judgment ... Class: minor under STND.IDENT.3 ... while no prime directive ... changes in its fundamental motivation or intent".

Problem: STND.IDENT.3 makes a change major if it alters a prime directive "in its fundamental motivation or intent". PRIME.8's motivation is that spending proceeds only on an owner-authorized estimate; the draft lets cost proceed with none. PRIME.9 reverses an explicit "NEVER ... even within an isolated environment". PRIME.13 adds a permission that prevails over three other prime directives. The comparison to revisions 1.5 and 1.7 (GUARD.7 and GOV.13, not prime directives) is weak. The ledger text also says "ratified by the custodian" (acceptable only because the script runs after ratification; keep).

Fix: either amend L1 so that the bound argument holds, or present the class to the custodian as doubtful with STND.IDENT.4 (the nearer-the-top class governs under doubt) and ask the custodian to rule the class. Do not assert the argument as settled.

### L3 (Medium) PRIME.11 and PRIME.8: a named person's reach is not limited the same way

Quote: "directly or through a person whom the human owner names under PRIME.11, the direction authorizes the operating cost" and "from a person whom the human owner names by a recorded act, within the scope that the act names".

Problems:
1. PRIME.8 lets a named person's direction authorize cost without the PRIME.11 scope limit repeated, and PRIME.11 says a named person performs none of the PRIME.1 acts (which include granting authorizations). PRIME.8 says the authorization comes "by this provision", so the conflict resolves toward authorizing cost, but a scope that names no spending still reads as authorizing it.
2. Nothing says a named person names no one else. "an agent directing it within an authority traceable to a directive ... of a person so named" lets a named person direct agents, and an agent could treat a named person's request to "also let Dana instruct you" as a naming.
3. "recorded act" does not say whose. An agent writing the record (scribe route) of an injected message could pass as the act.

Fix: PRIME.11: "A person so named names no other person and performs none of the acts that PRIME.1 assigns to the human owner." and "from a person whom the human owner names by an act of the human owner that is recorded". PRIME.8: "through a person whom the human owner names under PRIME.11, within the scope of that naming".

### L4 (Medium) GUARD.10: expired or revoked authorization keeps acting

Quote: "After an authorization expires or is revoked, an agent takes under it only the steps that leave the work in a safe and recoverable state (GUARD.3)."

Problem: "takes under it" continues the expired authorization for a class of steps judged by the agent. GUARD.10 itself says an authorization names a duration, and PRIME.7 says an authorization is never inferred or extended by the agent. GUARD.3's "within its authority" is the safe wording; this sentence widens it to the lapsed authority.

Scenario: the owner revokes a push or network authorization because a credential leaked or the agent misbehaved. The agent, mid-way through a multi-step remote write, finishes "to leave the remote recoverable" under the revoked grant. The rationale lists this as a residual risk, but it is avoidable.

Fix: "After an authorization expires or is revoked, an agent takes no further action under it, and takes only the steps that GUARD.3 permits within the authority that remains." Add that a revocation for cause (the owner says so) leaves only local steps.

### L5 (Medium) GOV.14: weakens the class-growth safeguard

Quote: "The class that the human owner records governs until the human owner reclassifies the work ... An agent that finds that reliance on the work or its exposure has grown refers that growth to the human owner."

Problems:
1. "refers" without "halts" is not a term of art here (PRIME.14 halts a line and refers). It is unclear whether the agent halts (a new halt at CSQ3/CSQ4) or continues. Both readings are bad: halt on every finding of growth at CSQ4, or continue at the stale class.
2. With a recorded low class and known severe reliance, the draft has the recorded class govern. GOV.13's "known more severe use" exclusion applies only when no class is recorded. STND.CLASS.7 still says reliance "SHALL NOT" occur until reassessment but now instantiates a GOV.14 that no longer anchors it.

Scenario: CSQ4 notebook becomes a dependency of a CSQ1 service; the owner never reclassifies; the agent keeps working at CSQ4 obligations and sends a note.

Fix: "An agent that finds that reliance on the work or its exposure has grown refers that growth to the human owner (PRIME.14), and does not support the more severe use until the human owner records the class." This halts only the line that supports the more severe use, which GOV.13 already does for unrecorded classes.

### L6 (Medium) GOV.13 presumption: "knows" and the untouched QA.11 and Notes

Quote: "That presumption NEVER covers driving physical hardware, or a use made of the work that an agent knows to be more severe than CSQ4."

Problems:
1. "knows" is the weakest standard and a subjective one; work that is in fact severe, in a project nobody classified, is treated as CSQ4 unless the agent happens to know. GOV.9 resolves doubt toward the more restrictive reading only for permissions, not for "knows".
2. QA.11 is unchanged: for CSQ3/CSQ4 "the adopted classification is the promotion". With no adopted classification there is no promotion, so the first relied-upon result still needs an owner act. GOV.20's new sentence ("a promotion (QA.11) and a release (QA.10) are acts of the human owner, recorded under the defaults") makes that explicit, but it reads as an act in addition to the classification, even where the classification exists. That could add an owner decision per promotion at CSQ3/CSQ4 (see L8).
3. Notes that contradict: `STND/DFLT/_doc.md` (line 62 "No class is set by default (GOV.13)" and line 66 "No class is assumed (GOV.13)"). Line 66 now contradicts "treated as CSQ4". The draft names STND.DFLT Notes only for PRIME.8; the GOV.13 and GOV.22 conforming is not named in the round decisions, and STND.CLASS.18/19 rows for an unclassified project are also silent.

Fix: GOV.13: "or a use made of the work that the request, the record, or the work itself shows to be more severe than CSQ4." Add STND.DFLT Notes lines 62 and 66 to the lower-governance list of the rationale.

### L7 (Medium) PRIME.9: "isolated environment" is undefined and unrecorded

Quote: "It uses superuser or administrative privilege only where the human owner provisioned that privilege within an isolated environment."

Problem: the owner decides what is provisioned, but not whether the environment is isolated in any recorded way. An agent can conclude "container, therefore isolated" when the container mounts the home directory, holds a container-runtime socket, or has network reach, so root there is root over the host. The draft rejected defining isolation in LVL0; fine, but a record is cheap.

Fix: "only where the human owner provisioned that privilege within an environment that the human owner has recorded as isolated"; where there is no such record the agent refers (PRIME.14). The LEX term Elevated privilege takes the same wording.

### L8 (Low) GOV.20: second sentence adds an act and drops CSQ2

Quote: "In a project without one, a promotion (QA.11) and a release (QA.10) are acts of the human owner, recorded under the defaults (GOV.22)."

Problems: QA.11 says that at CSQ3/CSQ4 the adopted classification is the promotion, so the sentence restates and may be read as requiring a second act. Projects of CSQ2 no longer get a constitution (decided, so not a defect), but then CSQ2 promotion also lacks the constitution's independence mechanisms and relies only on defaults; confirm that STND.DFLT covers QA.8 independence at CSQ2.

Fix: "a promotion other than through the adopted classification (QA.11), and a release (QA.10), are acts ..." and cut "(GOV.22)" duplication per GOV.31.

### L9 (Low) PRIME.13 safe state: permission reaches the network and removes every check

Quote: "An agent MAY command the designed safe state whenever it chooses, a step under GUARD.3 included, without further authorization and without a safe range of actuation or an estimate. This permission prevails over PRIME.6, PRIME.7, and PRIME.8."

Analysis: "designed safe state" is anchored by sentence 2 (designed, default on fault, verified before first driving), so a label alone does not qualify; with no hazard analysis the agent cannot drive the hardware at all. Residual: the override of PRIME.7 and PRIME.6 also covers network access and remote writes used to reach the device, and the irrecoverable side effects of the state (loss of unsaved data, a discarded batch), which the hazard analysis may not have weighed. This is the intended outcome of R2; I note the scope only.

Fix (optional narrowing): "by the means that the hazard analysis designates", so the permission reaches no other channel.

### L10 (Low) Drafting

1. GUARD.14 still reads "such as a per-task estimate or an operating envelope" in a provision this round amended; the custodian's direction bars "such as". Fix: "The human owner MAY set the discipline that governs it, a per-task estimate or an operating envelope included, and the choice is recorded."
2. PRIME.8: "or another limit that the human owner sets or the environment enforces" does not say a spending limit; an owner-set time, rate, or token-window limit then halts work at CSQ3/CSQ4. Say "another spending limit".
3. PRIME.11: "A person so named performs none of the acts that PRIME.1 assigns" is a prohibition without a modal; use "NEVER performs".
4. GUARD.1: "that its instructions call for, or that the unit of work they direct needs": "they" is ambiguous; use "or that the unit of work that its instructions direct needs".
5. GOV.22 last sentence restates GOV.13 ("is treated as GOV.13 provides"); GOV.31 asks for a citation only. Cut or reduce to "(GOV.13)".
6. "Operating cost" has no Lexicon entry except through Operating envelope; "own operating cost" may be read to include paid third-party services an agent calls (metered capacity). GOV.9 resolves to the restrictive reading, but add to LEX.implicit-expenditure or a new term: "the cost of running the agent, not of any other service it uses".
7. LEX.definition-of-done: "recorded or stated in the request" against QA.1 "recorded before the work is executed" — acceptable only if the request is itself a record. Add "the request being a record of the unit".

## Checked and sound

- GUARD.8 network-only: local bulk destruction stays reserved by GUARD.6 and GUARD.5; exfiltration needs network access or a remote write (GUARD.13 covers the tool channel), both authorization-bound with named volume; local secret reads stay under PRIME.10. LEX.bulk-retrieval matches.
- GUARD.9 exemption: limited to classes the register records under GUARD.7, which excludes history rewrite, and GUARD.6 prevails.
- GUARD.7 wording change: same sense; GUARD.5 still applies where no exempt class holds.
- GUARD.1 widening: remains reversible, local, within provisioned privilege, and the second sentence (installation, network, remote write, actuation, expenditure) still binds; only the L10.4 ambiguity.
- PRIME.9 split: acquiring or escalating is barred; LEX.elevated-privilege now matches; sentence three keeps the outside-environment bar.
- PRIME.14 and GOV.13: coherent; no new halt beyond the previous case (hardware or known severe use with no class recorded); GOV.13 dropped GOV.10 from `cites` correctly.
- GOV.10 and QA.1: narrows tests to work that changes code or data; PRIME.13's hazard analysis and evidence stay a prime directive. No safeguard falls.
- GOV.48: INTPR.11 at the level GOV.10 and GOV.11 set; PRIME.13 stays at every class for hardware.
- Explicit monetary transactions stay reserved in PRIME.6; PRIME.8 does not touch them.
- Precedence: PRIME.13's "prevails over" is explicit, so GOV.5/6 equal-rank restrictive reading does not defeat it.
- No new halt or owner decision at CSQ3/CSQ4 except those named in L5 and L8, both of which the fix wording removes.
- Titles unchanged; `cites` fields match the added references; ledger, manifests and revision row mechanically consistent; the revision row makes no claim that the custodian ruled anything.

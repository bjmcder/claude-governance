"""Content of the LVL2 round, draft 0.2 after the cold and pair reviews.

Each document is a dict: the fields of its _doc.md, its informative
sections in order, and its provisions. Rank and waivability are not
written here; build.py derives them from the corpus (GOV.17).
"""

DATE = "2026-10-20"


def P(n, title, section, body, inst, refs=(), mode="default", reason=None,
      defines=(), checked=("review",)):
    return dict(n=n, title=title, section=section, body=body.strip(),
                instantiates=list(inst), refers_to=list(refs), mode=mode,
                binding_reason=reason, defines=list(defines),
                checked_by=list(checked))


NORMATIVE = ("The body of a numbered provision, including a table it "
             "contains, is normative. Everything else is informative.")
TERMS_LEAD = ("This section fixes meaning and imposes no obligation, as the "
              "Lexicon does.")

# ================================================================ STND.DFLT
DFLT_NEW = [
    P(28, "Workbench directory", "Records", """
The workbench SHALL be the directory "workbench" in the directory of STND.DFLT.2, with each tool of AGENT.36 in its subdirectory "tools" and each other entry outside that subdirectory (GOV.22, AGENT.35, AGENT.36, REPRO.12, REPRO.10, INTPR.13).
""", ["GOV.22", "AGENT.35", "AGENT.36", "REPRO.12", "REPRO.10", "INTPR.13"], refs=["STND.DFLT.2"], mode="binding"),
    P(29, "Secret store directory", "Safeguards", """
Where the human owner provides a store of AGENT.44 for the work, that store SHALL be the directory "secrets" at the top of the work, holding each secret in a file of its own whose name contains no secret (GOV.22, AGENT.44, GUARD.16). That directory SHALL be created empty and recorded as a temporary location at its creation (GOV.22, GUARD.7).
""", ["GOV.22", "AGENT.44", "GUARD.16", "GUARD.7"], mode="binding"),
    P(30, "Secret store confirmation", "Safeguards", """
Before an agent first writes to the directory of STND.DFLT.29 in a session, it SHALL confirm that version control excludes the directory and that its permissions let no account read it other than the agent's own and accounts with superuser privilege (GOV.22, PRIME.10). Where either condition fails, the agent SHALL restore it within its provisioned privilege (GOV.22, PRIME.10). Where the agent is unable to confirm both after that, it SHALL refer the line of work that needs the store, without writing to the directory (GOV.22, PRIME.14).
""", ["GOV.22", "PRIME.10", "PRIME.14"], refs=["STND.DFLT.29"], mode="binding"),
    P(31, "Secret store exclusions", "Safeguards", """
Each copy of the work that an agent makes for an archive or a backup, or for a transfer beyond the provisioned environment, SHALL exclude the directory of STND.DFLT.29 (GOV.22, PRIME.10). Each recursive or pattern-selected operation that an agent applies to the top directory of the work SHALL exclude that directory, other than one that an authorization permits the agent to apply to the store (GOV.22, PRIME.10).
""", ["GOV.22", "PRIME.10"], refs=["STND.DFLT.29"], mode="binding"),
]

DFLT17_OLD = ("An agent SHALL enter each authorization that the human owner gives it directly as a ledger entry with itself as actor and the grant quoted (GOV.22, GUARD.10).")
DFLT17_NEW = ("An agent SHALL enter each authorization that the human owner gives it directly as a ledger entry with itself as actor and the grant quoted without each secret that the grant contains (GOV.22, GUARD.10, PRIME.10).")
DFLT17_OLD_INST = 'instantiates: ["GOV.22", "GUARD.2", "GUARD.10"]'
DFLT17_NEW_INST = 'instantiates: ["GOV.22", "GUARD.2", "GUARD.10", "PRIME.10"]'

DFLT_EDITS = [
    ("| Temporary location | A directory created empty for intermediates, recorded as temporary at creation, outside \"records\" and the version-control metadata. |",
     "| Temporary location | A directory created empty for intermediates, or for working copies of items whose source lies outside the work, recorded as temporary at creation, outside \"records\" and the version-control metadata. |"),
    ("A domain is within the bounds only with the purpose and volume an authorization names (GUARD.13). |",
     "A domain is within the bounds only with the purpose and volume an authorization names (GUARD.13). A file of the directory of STND.DFLT.29 is within the bounds only for an agent that an authorization permits to handle the secret that the file holds (PRIME.10). |"),
    ("It also gives the vocabulary of access descriptors that AGENT.23 leaves to the defaults.",
     "It also gives the vocabulary of access descriptors that AGENT.23 leaves to the defaults, and the locations of the workbench and, where the human owner provides one, of the store of non-credential secrets, which AGENT.35 and AGENT.44 leave to the project."),
    ("| Workspace (INTPR.5) | STND.DFLT.6 |",
     "| Workspace (INTPR.5) | STND.DFLT.6 |\n| Workbench (AGENT.35) | STND.DFLT.28 |\n| Store of non-credential secrets (AGENT.44) | STND.DFLT.29 to STND.DFLT.31 |"),
    ("STND.DEPS and STND.PROJ are to conform to this standard (GOV.42).",
     "The workbench (STND.DFLT.28) sits with the other records, so that it is kept under version control and retained with them, as AGENT.35 and AGENT.36 ask; its tools, which are repaired in place, sit apart from its entries, which are never altered (AGENT.34), so that a reviewer and a check of alteration tell them apart.\n\n"
     "The work keeps a store of non-credential secrets only where the human owner chooses to provide one, by an instruction or a ledger entry; STND.DFLT.29 to STND.DFLT.31 then apply, and otherwise ask nothing. The choice is the human owner's own and no provision asks for it (STND.DRAFT.42). Without a store, an agent that an authorization permits to handle such a secret writes it to no location (AGENT.44). Where provided, the store (STND.DFLT.29) sits at the top of the work, outside \"records\", \"notes\", and version control, as AGENT.44 asks; an authentication credential never enters it (AGENT.45). It holds working copies of the secrets that the work is authorized to use, one per file, so that the working bounds admit each file only to an agent authorized to handle its secret: such an agent reads and writes it without a referral, and every other agent that reaches for it halts and refers (STND.DFLT.25). The directory is a temporary location, as the term now admits for working copies whose source lies outside the work, so that removing a secret the work no longer needs, as AGENT.44 asks, is the removal of a temporary item (STND.DFLT.15) rather than a reserved action; for the same reason no record cites a file of the store, and a record names a secret by a description that is itself no secret. The store holds only working copies whose source is the grantor of the secret, so AGENT.37 is met. Before its first write in a session an agent confirms that version control excludes the directory and that no other unprivileged account reads it, restores either condition that fails, which is a reversible local action, and refers rather than writing only where it is still unable to confirm (STND.DFLT.30). Archives, backups, and transfers leave the directory out, so the archive of STND.DFLT.4 carries no secret, and recursive and pattern-selected operations skip it unless authorized for it, so that a search of the work neither reads a secret nor halts on one (STND.DFLT.31). A grant that contains a secret is entered in the ledger without that secret (STND.DFLT.17). A project constitution states its own locations, or adopts these by citation. A harness that derives an environment under STND.HARN.18 maps the bounds of the store as STND.DFLT.29 and the working bounds state them."),
]
DFLT_ROW = ("| 1.5 | " + DATE + " | Minor amendment (GOV.41), conforming on the adoption of AGENT: new STND.DFLT.28 places the workbench in the directory \"workbench\" of the records directory, its tools in \"tools\"; new STND.DFLT.29 to STND.DFLT.31 place the store of non-credential secrets of AGENT.44, where the human owner provides one, in the temporary directory \"secrets\" at the top of the work, one secret per file, have an agent confirm before its first write in a session that version control excludes it and that no other unprivileged account reads it, restoring either condition where it fails, and keep it out of archives, backups, transfers, and unauthorized recursive or pattern-selected operations; the working bounds admit each file of the store only to an agent authorized to handle its secret; STND.DFLT.17 enters a grant without the secrets it contains; the term Temporary location admits working copies of items whose source lies outside the work. |")

# =============================================================== STND.INSTR
INSTR9 = P(9, "Research placement", "Documentation", """
An agent SHALL keep its research notes, the findings of AGENT.32, and the entries it holds under AGENT.30 in the workbench, and not only in the working-notes workspace (GOV.48, AGENT.30, AGENT.31, AGENT.32, INTPR.13, REPRO.11).
""", ["GOV.48", "AGENT.30", "AGENT.31", "AGENT.32", "INTPR.13", "REPRO.11"], mode="binding")
INSTR_EDITS = [
    ("It holds only practice that LVL0 and STND.DFLT state as outcomes.",
     "It holds only practice that LVL0, AGENT, and STND.DFLT state as outcomes."),
    ("The earlier draft's default standing authorization is dropped,",
     "STND.INSTR.9 decides only where research material goes, so at every class it asks no record that AGENT does not already ask; a note of a change outside scope (AGENT.19) stays in the working-notes workspace. The earlier draft's default standing authorization is dropped,"),
]
INSTR_ROW = ("| 1.3 | " + DATE + " | Minor amendment (GOV.41), conforming on the adoption of AGENT: new STND.INSTR.9 keeps research notes, the findings of AGENT.32, and the entries held under AGENT.30 in the workbench, and not only in the working-notes workspace. |")

# ================================================================ STND.CODE
CODE = dict(
    id="STND.CODE", title="Coding standard",
    instantiates=["GOV.18", "GOV.19"],
    sections=[
        ("Purpose and scope", """This standard holds the coding practice that applies to source in every language, hardware descriptions included, as outcomes that a tool or a reviewer decides from the source, its repository configuration, and its record of checks. It adds to DSGN, SIMPL, INTPR, REPRO, VV, QA, and PRIME.4 only what makes their outcomes checkable at each change. The language standards that the mnemonic register reserves for Python, C++, and Julia, once adopted, add the conventions of each language. STND.CODE.6 and STND.CODE.7 instantiate PRIME.4, so they are binding and apply at every class; every other provision is a default (GOV.19) and a recommendation, which a project replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7, PRIN.10). No provision names a language, tool, or method (GOV.18)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """

| Term | Definition |
| --- | --- |
| Repository configuration | The versioned files of the work that set how its tools build, check, format, and test it, apart from its governance. |
| Static check | A check of source or of a build that the means of the work make without running the work. |
| Execution setting | An option, flag, or variable of a compiler, interpreter, build, or run that changes which code executes. |"""),
        ("Notes", """Each default provision asks for the cheapest evidence that keeps an outcome of LVL0 from failing silently. A tool that looks for cycles at each change keeps DSGN.7 true as the code grows (STND.CODE.1). Inputs that change between runs, the source of randomness and the run settings included, arrive through the interface, so that DSGN.14, DSGN.16, and DSGN.17 are visible at the call; a named constant, a hardware parameter fixed at synthesis, and a fixed configuration of a constrained target are not such inputs (STND.CODE.2). A contract stated at the declaration, or a citation of the one place that declares its units and conventions, puts DSGN.1 and INTPR.4 where every reader of the interface passes (STND.CODE.3).

The repository configuration names the static checks that the languages of the work offer, and each change passes them; a finding left in place is suppressed where it occurs, with its reason, so that the reason is the decision record of REPRO.7 (STND.CODE.4). A suppression records an accepted finding; it is not a way to pass a check (PRIME.2, AGENT.47). An agent that weakens a check or a setting in the change that the check judges records the two apart (AGENT.5) and states the weakening in its work report (AGENT.47). A layout that a named tool produces and confirms costs the reviewer nothing (STND.CODE.5).

STND.CODE.6 and STND.CODE.7 rest on PRIME.4 and bind at every class, CSQ4 included, a tightening of PRIME.4 at the cost of one look at one location (PRIME.15). A check of untrusted input that an execution setting removes, as an assertion compiled out of an optimized build is, lets invalid input pass silently in the builds that run in production. A failure of a kind that PRIME.4 lists is never discarded (STND.CODE.7). Another failure that code discards carries, at that location, the reason the results stay correct, which a reviewer checks (STND.CODE.12, a default). HW.8 and HDES add the responses that hardware asks for.

A test added for each fixed defect (STND.CODE.8) is a regression guard unless its reference is independent of the code it judges (VV.7); either way it lets VV.8 detect the defect's return. A test whose verdict changes between runs of the same revision, seeds included, gives no evidence, and a test whose reference is local needs no network access, which would otherwise call for an authorization (PRIME.7) (STND.CODE.9). A constant that a measurement, a published reference, or a recorded choice fixes carries its unit, source, and revision once (STND.CODE.10), while a literal of a formula, a loop bound, and an index origin are not such constants; a measured or calibrated constant is also versioned data under REPRO.6 and MEAS. Code disabled by turning it into a comment is neither active nor retired; the source history keeps it (STND.CODE.11, SIMPL.8).

Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or QA and applies from CSQ3; work of CSQ4 omits it. No default provision raises the floor (GOV.11). Hardware descriptions are code under this standard; HDES governs what their verification shows."""),
    ],
    provisions=[
        P(1, "Mechanical cycle check", "Structure", """
At each change to the dependency structure of the work's components, a tool SHOULD check that structure for cycles (DSGN.7).
""", ["DSGN.7"]),
        P(2, "Inputs through interfaces", "Structure", """
Each function that computes a result SHOULD receive through its interface each input that affects that result and changes between runs, its source of randomness and its run settings included (DSGN.14, DSGN.16, DSGN.17).
""", ["DSGN.14", "DSGN.16", "DSGN.17"]),
        P(3, "Contracts at declarations", "Structure", """
Each interface that another component uses SHOULD state, at its declaration, what it requires, guarantees, and preserves, with the units and conventions of the data it exchanges or a citation of the one place that declares them (DSGN.1, INTPR.4).
""", ["DSGN.1", "INTPR.4"]),
        P(4, "Static checks per change", "Checking", """
Where the tools of a language of the work offer static checking of types, units, or contracts, the repository configuration SHOULD name that checking (DSGN.3). Each change SHOULD pass the static checks that the repository configuration names, at the settings that it records (DSGN.3). Each finding of those checks that a change does not resolve SHOULD be suppressed at its location with its reason (REPRO.7).
""", ["DSGN.3", "REPRO.7"]),
        P(5, "Mechanical source layout", "Checking", """
The repository configuration SHOULD name, for each language of the work, a tool that produces the layout of its source (INTPR.1). At each change, each such tool SHOULD confirm that the source has the layout that it produces (INTPR.1).
""", ["INTPR.1"]),
        P(6, "Unremovable input checks", "Failures", """
A check that rejects invalid input where untrusted data enters SHALL NOT be removable by an execution setting (PRIME.4, DSGN.2).
""", ["PRIME.4", "DSGN.2"], mode="binding"),
        P(7, "Discarded failures", "Failures", """
Code SHALL NOT discard a failure of a kind that PRIME.4 lists (PRIME.4).
""", ["PRIME.4"], mode="binding"),
        P(8, "Regression test per fix", "Tests", """
Each fix of a defect in code SHOULD add a test that fails on the revision before the fix and passes on the revision after it (VV.8, QA.4).
""", ["VV.8", "QA.4"]),
        P(9, "Repeatable test verdicts", "Tests", """
Each test SHOULD give the same verdict on every run against the same revision and recorded inputs, its random seeds included (REPRO.3). Where a test's reference is inside the provisioned environment, the test SHOULD NOT reach outside it (REPRO.1, REPRO.3).
""", ["REPRO.3", "REPRO.1"]),
        P(10, "Named domain constants", "Source", """
Each numeric constant that a measurement, a published reference, or a recorded choice fixes, and on which a reported result depends, SHOULD be defined once, by a name, with its unit, its source, and its revision, and used by that name (INTPR.4, REPRO.6).
""", ["INTPR.4", "REPRO.6"]),
        P(11, "Disabled code in comments", "Source", """
Source SHOULD NOT hold code disabled by its conversion into a comment (SIMPL.8).
""", ["SIMPL.8"]),
        P(12, "Reasoned discards", "Failures", """
Where code discards a failure that it detects or receives and that PRIME.4 does not list, it SHOULD state at that location why discarding it leaves the results of the work correct (REPRO.7).
""", ["REPRO.7"], refs=["PRIME.4"]),
    ],
)

# ================================================================ STND.THRT
THRT = dict(
    id="STND.THRT", title="Threat-model template",
    instantiates=["GOV.21", "GUARD.16"],
    sections=[
        ("Purpose and scope", """This standard fixes the form and minimum content of the threat model that a project constitution holds (GUARD.16, GOV.21): a table of assets, threats, sources, and protection, carrying at least the rows of the defaults (STND.DFLT.18) and a row for compromise of fetched components; the protected data, the readers trusted with secrets, and the channel for reporting a secret (PRIME.10); how alteration of the records is detected (PRIME.5); the events that call for a proposal to review it; the separation of its sensitive part (GUARD.18); and two secure practices that every actor follows unless the threat model records an alternative (GUARD.17). Every provision but STND.THRT.8 instantiates a prime directive or GUARD, so it is binding and applies at every class; STND.THRT.8 is a default. No provision names a tool (GOV.18)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """

| Term | Definition |
| --- | --- |
| Asset | A thing of value to the work that a threat model names: source, data, results, records, credentials, hardware, people, or a system the work reaches. |
| Control | A means that prevents a threat to an asset or detects its occurrence. |
| Protected data | A location or kind of data that a threat model lists under STND.THRT.3. A row that the project protects names a protected asset, which is not by that alone protected data. |"""),
        ("Notes", """The rows of STND.DFLT.18 are the minimum because each protected row there rests on a prime directive: change beyond authority on PRIME.5 and PRIME.7, disclosure of secrets on PRIME.10, action beyond authorization on PRIME.7 and PRIME.9, injected instructions on PRIME.11 and GUARD.16, and fabricated evidence on PRIME.2. STND.THRT.2 adds the row for compromise of fetched components through their supply chain, against which the integrity and advisory provisions of the dependency policy are the controls. A fetched component is an asset the work depends on, so the row for fetched components governs for it over the row of STND.DFLT.18 that leaves compromise of the work and the provisioned environment unprotected. A project adds rows and protects more; it does not unprotect those. For a project whose constitution adopts this standard, STND.THRT.2, with the integrity and advisory provisions of the dependency policy, protects more than the default threat model of STND.DFLT.18; the consequence that warrants it is undetected compromise of a fetched component, and the constitution that cites these standards is the recorded decision (GOV.11). The rows that the project marks as not protected are the separate statement of what it does not attempt to protect (GUARD.16).

STND.THRT.3 makes concrete the protected data that PRIME.10 and the working bounds of STND.DFLT refer to, a store of AGENT.44 and its readers included where the work keeps one, and keeps the list readable, because an agent avoids only what it is able to see. It also names whom the threat model trusts with a secret, the test that the term Secret of AGENT and STND.THRT.4 rely on. STND.THRT.4 gives the secret-report channel of PRIME.10, which the threat model states as the human owner directly where it designates no other; the channel is one that no untrusted reader sees, so that the report does not itself disclose. STND.THRT.5 asks only that the project say how alteration is detected, by chained hashes, signatures, or another means of its choice.

The events of STND.THRT.6 always change exposure; GUARD.16 still asks for a review at every other change of exposure. A routine retrieval from a new site changes exposure only where the site is of a kind of source that the threat model does not name. The actor that brings an event about or learns of it records it and proposes the change it calls for; the human owner adopts the revised threat model, and every line of work that the event does not concern continues (AGENT.15). Coming to hold irreplaceable data, or an asset or source of threat that the model omits, is one of these events, the counterpart under a project constitution of STND.DFLT.19. A review before each release is recommended.

STND.THRT.7 keeps the sensitive part of a threat model apart, outside version control and every record and readable only by those the threat model trusts with it, so that the access controls of GUARD.18, to the extent the human owner records as practical, restrict only that part, while every actor reads the rest, which INTPR.12 needs. The part stays out of versioned records, because PRIME.10 bars secrets there; the rest cites it, and each change to it is entered in the ledger by reference (GOV.36). STND.THRT.8 is a default proportioned to class under REPRO.13, applying from CSQ3 under STND.CLASS.10.

STND.THRT.9 carries the two practices of the undivided draft it replaces that LVL0 does not already state: least privilege for each account, key, and token that the work provisions, and no weakening of a security or integrity check to make an action succeed, other than the recorded routes of QA.6, VV.3, and STND.CODE.4, each stated in the work report. The others, no secrets in source and records, validation of untrusted input, and integrity of fetched components, are PRIME.10, DSGN.2, and the dependency policy. Work without a project constitution uses the threat model of STND.DFLT.18 and STND.DFLT.19."""),
    ],
    provisions=[
        P(1, "Threat-model table form", "Content", """
A threat model SHALL state, in each row of a table, an asset, a threat to it, the source of that threat, and whether the project protects the asset against it (GUARD.16). Each row that the project protects SHALL name the controls on which that protection relies (GUARD.16, GUARD.17).
""", ["GUARD.16", "GUARD.17"], mode="binding"),
        P(2, "Rows carried from defaults", "Content", """
A threat model SHALL contain each row of the table of STND.DFLT.18 (GUARD.16). It SHALL mark as protected each row that the table of STND.DFLT.18 marks as protected (GUARD.16, PRIME.11). It SHALL also contain, marked as protected, the row of the table of this provision (GUARD.16, GUARD.17).

| Asset | Threat | Source | Protected |
| --- | --- | --- | --- |
| Fetched components that the work depends on | Compromise through their supply chain | Their publishers and the systems that serve them | Yes |
""", ["GUARD.16", "PRIME.11", "GUARD.17"], refs=["STND.DFLT.18"], mode="binding", defines=["added-rows"]),
        P(3, "Protected data list", "Content", """
A threat model SHALL list each location and each kind of data that it marks as protected, each store of AGENT.44 that the work keeps and the accounts that read it among them (PRIME.10, AGENT.44). That list SHALL stay readable by each actor of the project (PRIME.10, INTPR.12). A threat model SHALL name each person and system that it trusts with a secret (PRIME.10).
""", ["PRIME.10", "AGENT.44", "INTPR.12"], mode="binding"),
        P(4, "Secret-report channel", "Content", """
A threat model SHALL state the channel through which an actor reports to the human owner an incidental encounter with a secret (PRIME.10). That channel SHALL be one that only the human owner and those whom the threat model trusts with secrets read (PRIME.10).
""", ["PRIME.10"], mode="binding"),
        P(5, "Alteration detection for records", "Content", """
A threat model SHALL state how an alteration of the records, the source history, or the ledger is detected (PRIME.5, GOV.36).
""", ["PRIME.5", "GOV.36"], mode="binding"),
        P(6, "Exposure events", "Review", """
Where an actor brings about or learns of an event of the table of this provision, the actor SHALL record the event and propose to the human owner each change of the threat model that the event calls for (GUARD.16). A threat model SHOULD be reviewed before each release (GUARD.16).

| Event |
| --- |
| A new kind of hardware, instrument, or physical system that the work drives or reads |
| A new remote system to which the work writes, or a new provider of an agent or of computing |
| A new kind of source whose content an agent reads |
| A new collaborator with access to the work, its records, or its environment |
| A new kind of data, data that identify people included |
| A new source of dependencies |
| A change of the store of AGENT.44 or of the accounts that read it |
| The work comes to hold irreplaceable data, or an asset or source of threat that the threat model omits |
| An incident whose root cause the threat model omits |
""", ["GUARD.16"], refs=["AGENT.44"], mode="binding", defines=["exposure-events"]),
        P(7, "Sensitive threat-model part", "Protection", """
Where a threat model holds information whose disclosure would ease an attack, it SHALL keep that information apart from the rest, in a location outside version control and every record that only those whom the threat model trusts with it read, with a reference to it, and a means of detecting alteration of its content that discloses nothing of the part, in the rest (GUARD.18, PRIME.10). The rest of the threat model SHALL stay readable by each actor of the project (GUARD.18, INTPR.12).
""", ["GUARD.18", "PRIME.10", "INTPR.12"], mode="binding"),
        P(8, "Irreplaceable data copies", "Protection", """
For each irreplaceable dataset, the threat model SHOULD state the location of its independent recoverable copy and of the record of the last test of its recovery (REPRO.13).
""", ["REPRO.13"]),
        P(9, "Default secure practices", "Practice", """
Unless the threat model records an alternative that protects the same rows, each actor SHALL follow each practice of the table of this provision (GUARD.17).

| Practice |
| --- |
| Each account, key, and token that the work creates or provisions for an agent, a service, or an automated step holds only the privilege that its use needs. |
| Each check of verification, authentication, authorization, and integrity stays at its strength when an action fails it, other than by a decision recorded under QA.6, VV.3, or STND.CODE.4 that the actor's work report states. |
""", ["GUARD.17"], refs=["QA.6", "VV.3", "STND.CODE.4"], mode="binding", defines=["secure-practices"]),
    ],
)

# ================================================================ STND.KNOW
KNOW = dict(
    id="STND.KNOW", title="Knowledge base and tags",
    instantiates=["GOV.32", "GOV.33", "GOV.34", "GOV.37"],
    sections=[
        ("Purpose and scope", """This standard fixes what a knowledge entry states, its kinds and form, the evidence levels and the reliance ceiling of each, how an entry is established, revalidated, superseded, and retracted, how an entry drawn from a project's workbench is made and reconciled, and the permanence and use of tags (GOV.32 to GOV.34, GOV.37). GOV.33 assigns the ceiling of each evidence level to a LVL2 standard; STND.KNOW.5 sets it. Every provision but STND.KNOW.12 and STND.KNOW.14 is binding, because it instantiates GOV, which the floor holds (GOV.10), or a prime directive, and a knowledge base shared across projects is read the same way by each of them; STND.KNOW.12 and STND.KNOW.14 are defaults (GOV.19) that apply from CSQ3. A provision imposes nothing on work that keeps and consults no knowledge entry. No provision names a tool (GOV.18)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """ Lesson, Research note, Reusable finding, and Workbench have the meanings that AGENT gives them; Protected data has the meaning that STND.THRT gives it.

| Term | Definition |
| --- | --- |
| Drawn entry | A knowledge entry whose claim a workbench entry or a research note of a project stated first. |
| Establishing review | The review of GOV.34 by which a knowledge entry becomes established. |
| Revalidation | A confirmation, after an entry is established, that its evidence still meets its evidence level over its domain of validity. |
| Facet | One part of the tag vocabulary, holding the tags of one kind of subject. |"""),
        ("Notes", """The evidence levels follow the names the Lexicon gives them, and each asks of its evidence what STND.CLASS.10 asks of VV.1 at the class of its ceiling. EVD0 asks that an actor other than the author regenerate the evidence from its records, as QA.9 asks from CSQ1. EVD1 holds evidence that meets VV.1 as applied at CSQ2, over the entry's whole domain of validity, a cited source confirmed under VV.2 included, which VV.1 counts as evidence. EVD2 holds partial evidence and sources not yet confirmed. EVD3 holds the rest. The ceilings step one class per level, from CSQ1 for EVD0 to CSQ4 for EVD3. No level carries reliance at CSQ0 without fresh verification, because STND.CLASS.10 asks safety-related components for proof, exhaustive checking, or an independent reference, which a knowledge entry is not. The independence of the establishing review also caps the ceiling (STND.KNOW.7), following the rows of STND.CLASS.18 read for the review of an entry: a human reviewer admits CSQ1, an agent of another configuration that the author does not direct admits CSQ2, and every other reviewer CSQ3, whatever the evidence. Because STND.CLASS.10 gives VV.1 the same content at CSQ1 and CSQ2, EVD0 and EVD1 differ by the regeneration of the evidence by another actor. Reliance above a ceiling needs the evidence that VV asks at the class concerned (GOV.33); the entry still informs the work.

STND.KNOW.6 never blocks work. An entry not yet established, one whose revalidation is overdue, and one relied on outside its stated domain of validity keep informing exploratory work and are relied on above CSQ4 only with fresh evidence. The step to CSQ4 on an overdue revalidation is deliberate: it costs nothing until reliance is sought, and then asks only the revalidation that restores the ceiling. The recommended interval of revalidation, at most 24 months, is a recommendation inside a binding provision; a knowledge base that records another interval departs from it by a recorded decision (PRIN.10). An entry is never altered in place (GOV.34), so its status follows from the records that cite it: the establishing review, each revalidation, whose stated next date governs over the earlier one, and each entry that supersedes or retracts it. A listing generated from those records shows that status for lookup, and is informative (GOV.39). Each supersession and retraction is notified to everything that relies on the entry (GOV.34, QA.13).

The workbench has the reach of one project (AGENT). A drawn entry therefore carries its evidence with it, or cites a record that every reader of the knowledge base retrieves, and names its source project by a reference that is not protected data, so that a reader of another project judges it without that project's records (STND.KNOW.10). No knowledge entry carries a secret, information from which a secret is inferred, or the protected data of the project it comes from (STND.KNOW.11), because a knowledge base reaches readers whom that project's threat model does not name (AGENT.43). An entry cites external material rather than reproducing it, so that the license terms of the material govern only its source. Once a knowledge base establishes an entry that a workbench held under AGENT.30, an agent of the project that learns of it records that fact by a new workbench entry (STND.KNOW.12), because AGENT.34 forbids altering the old one; later work relies on the established entry as knowledge, and on the workbench entry only as evidence. A proposal held in a workbench carries the project's name and a number of that workbench, and takes an identifier of the knowledge base only on establishment (STND.KNOW.3), so that two projects never number the same identifier.

The kinds of STND.KNOW.2 follow the items that AGENT.26 and AGENT.27 ask agents to propose, and add the dependency set that the dependency policy leaves to the knowledge base: a set of external components that has served together across projects, with the regime in which it served. An entry of kind Result states whether its result is promoted and whether it is unverified, as AGENT.27 asks of the proposal (STND.KNOW.1). A knowledge entry for a tool describes the tool and states where it is kept; the tool is not itself an entry (custodians' interpretation of GOV.32, 2026-10-11).

Which knowledge base serves a project is stated in its project constitution or, where none is designated, AGENT.30 holds proposed entries in the workbench. The space KNOW of the governance corpus, with one directory per domain (STND.IDENT.15), and the tag vocabulary TAG, with one directory per facet, are the custodians' shared knowledge base and tags. A facet is registered as a mnemonic (STND.IDENT.19); a tag is added by a file in its facet's directory. The facet TAG.COMP is local to a project."""),
    ],
    provisions=[
        P(1, "Knowledge entry content", "Entries", """
Each knowledge entry SHALL state its claim, its kind, its evidence, its evidence level, its domain of validity, its author, its date, and the schedule of its revalidation (GOV.33, GOV.34). An entry of kind Result SHALL state whether the result is promoted and whether it is unverified (QA.11, PRIME.3).
""", ["GOV.33", "GOV.34", "QA.11", "PRIME.3"], mode="binding"),
        P(2, "Knowledge entry kinds", "Entries", """
The kind of a knowledge entry SHALL be exactly one kind of the table of this provision (GOV.32).

| Kind | Claim |
| --- | --- |
| Lesson | A lesson, with the units of work or the trend that reveal it |
| Method | A method or practice and the regime in which it serves |
| Tool | What a tool does, the regime in which it serves, and where it is kept |
| Result | A research result |
| Negative result | An approach that failed, and the conditions under which it failed |
| Anomaly | An explained anomaly and its cause |
| Dependency set | A set of external components that served together, and the regime in which it served |
| Other finding | A reusable finding of no other kind of this table |
""", ["GOV.32"], mode="binding", defines=["entry-kinds"]),
        P(3, "Knowledge entry form", "Entries", """
Each knowledge entry SHALL be kept as a plain-text file under version control (GOV.32, REPRO.12). An entry of a knowledge base SHALL carry an identifier of the form that STND.IDENT.15 gives (GOV.37). An entry that a workbench holds under AGENT.30 SHALL carry the name of its project and a number that no other entry of that workbench carries (GOV.37, AGENT.30, INTPR.13).
""", ["GOV.32", "GOV.37", "REPRO.12", "AGENT.30", "INTPR.13"], refs=["STND.IDENT.15"], mode="binding"),
        P(4, "Evidence level assignment", "Reliance", """
A knowledge entry SHALL take the first evidence level, in the order of the table of this provision, whose evidence the entry's evidence meets (GOV.33).

| Level | Name | Evidence |
| --- | --- | --- |
| EVD0 | Verified | Evidence that meets VV.1, as STND.CLASS.10 applies it at CSQ1, over the whole stated domain of validity, regenerated from its records by an actor other than the entry's author (QA.9) |
| EVD1 | Confirmed | Evidence that meets VV.1, as STND.CLASS.10 applies it at CSQ2, over the whole stated domain of validity |
| EVD2 | Reported | Evidence that meets VV.1 for at least one case within the stated domain of validity, or a cited source not yet confirmed under VV.2 |
| EVD3 | Anecdotal | Every other support, an observation or an experience without a record that meets VV.1 included |
""", ["GOV.33"], refs=["VV.1", "VV.2", "QA.9", "STND.CLASS.10"], mode="binding", defines=["evidence-levels"]),
        P(5, "Reliance ceilings by level", "Reliance", """
Except as STND.KNOW.6 and STND.KNOW.7 provide, the reliance ceiling of a knowledge entry SHALL be the consequence class that the table of this provision gives for its evidence level (GOV.33).

| Level | Reliance ceiling |
| --- | --- |
| EVD0 | CSQ1 |
| EVD1 | CSQ2 |
| EVD2 | CSQ3 |
| EVD3 | CSQ4 |
""", ["GOV.33"], refs=["STND.KNOW.6", "STND.KNOW.7"], mode="binding", defines=["reliance-ceilings"]),
        P(6, "Provisional reliance ceiling", "Reliance", """
Until a knowledge entry is established, its reliance ceiling SHALL be CSQ4 (GOV.33, GOV.34). While a revalidation of an established knowledge entry is overdue under its schedule, its reliance ceiling SHALL be CSQ4 (GOV.33, GOV.34). For reliance outside its stated domain of validity, the reliance ceiling of a knowledge entry SHALL be CSQ4 (GOV.33).
""", ["GOV.33", "GOV.34"], mode="binding"),
        P(7, "Establishing review record", "Lifecycle", """
The establishing review of a knowledge entry SHALL confirm that the entry's evidence meets its evidence level over its stated domain of validity (GOV.33, GOV.34). The record of that review SHALL cite the entry and state the revision reviewed, the reviewer, and the verdict (GOV.34). The reliance ceiling of the entry SHALL be no more severe than the class that the table of this provision gives for the actor that performed its establishing review (GOV.33, QA.8).

| Establishing reviewer | Most severe ceiling |
| --- | --- |
| A human other than the entry's author | CSQ1 |
| An agent not directed by the author and of an agent configuration other than the author's | CSQ2 |
| Another actor other than the author | CSQ3 |
""", ["GOV.33", "GOV.34", "QA.8"], mode="binding", defines=["reviewer-ceilings"]),
        P(8, "Revalidation schedule", "Lifecycle", """
The schedule of revalidation of a knowledge entry SHALL name the events after which its evidence no longer holds, and the date of its next revalidation (GOV.34). That date SHOULD fall at most 24 months, inclusive, after the entry was established or last revalidated (GOV.34). Each revalidation SHALL be recorded in a record that cites the entry and states the evidence level it confirms and the date of the next revalidation (GOV.34).
""", ["GOV.34"], mode="binding"),
        P(9, "Superseded and retracted entries", "Lifecycle", """
Where a revalidation or a later finding shows that the evidence of a knowledge entry no longer meets its evidence level, a new entry SHALL supersede or retract it (GOV.34). The superseding or retracting entry SHALL cite the entry it supersedes or retracts (GOV.34). The superseded or retracted entry SHALL remain in the knowledge base unaltered (GOV.34).
""", ["GOV.34"], mode="binding"),
        P(10, "Drawn entry sources", "Workbench entries", """
A drawn entry SHALL name, by a reference that is not protected data, the project whose workbench holds the workbench entry or research note that it cites (GOV.32, AGENT.38). A drawn entry SHALL state its evidence in itself or in a record that each reader of the knowledge base is able to retrieve (GOV.33).
""", ["GOV.32", "GOV.33", "AGENT.38"], mode="binding"),
        P(11, "Secrets in knowledge entries", "Workbench entries", """
A knowledge entry SHALL NOT contain a secret (PRIME.10). A knowledge entry SHALL NOT contain information from which a secret is able to be inferred (PRIME.10, AGENT.43). A knowledge entry SHALL NOT contain protected data of the project from which it comes, as that project's threat model lists it under STND.THRT.3 (PRIME.10).
""", ["PRIME.10", "AGENT.43"], refs=["STND.THRT.3"], mode="binding"),
        P(12, "Established workbench proposals", "Workbench entries", """
Where an agent of a project learns that a knowledge base has established an entry that the project's workbench holds under AGENT.30, the agent SHOULD record in that workbench a new entry that cites the identifier of the established entry (AGENT.30, INTPR.13).
""", ["AGENT.30", "INTPR.13"]),
        P(13, "Tag permanence", "Tags", """
A tag SHALL NOT be removed from the tag vocabulary (GOV.37). A deprecated tag SHALL name the tag that replaces it, or state that no tag replaces it (GOV.37).
""", ["GOV.37"], mode="binding"),
        P(14, "Tags on knowledge entries", "Tags", """
Each knowledge entry SHOULD carry the tags of the tag vocabulary that name its subject, its method, and each hardware type it concerns (AGENT.28, QA.2).
""", ["AGENT.28", "QA.2"]),
    ],
)

# ================================================================ STND.DEPS
DEPS = dict(
    id="STND.DEPS", title="Dependency policy",
    instantiates=["GOV.19", "GOV.21"],
    sections=[
        ("Purpose and scope", """This standard is the dependency management mechanism (REPRO.9) that a project constitution adopts by citation or replaces with tighter rules, and the policy for weighing a dependency (SIMPL.4). It states how a dependency is chosen, which revision is pinned and when it is reviewed, how fetched components are verified, and what the dependency record holds. STND.DEPS.6 and STND.DEPS.7 instantiate GUARD.17, against the supply-chain row that STND.THRT.2 adds to every threat model, so they are binding and apply at every class; every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7). No provision asks the human owner for a decision; selection, pinning, and review are the work of whoever changes the dependency (STND.DRAFT.42). No provision names a tool (GOV.18)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """

| Term | Definition |
| --- | --- |
| Dependency record | The enumeration of external components that REPRO.9 requires, with their revisions, license identities, and reasons. |
| Fetched component | An external component that the work depends on and that an actor transfers into the provisioned environment from a system outside it. |
| Integrity digest | A cryptographic hash of the exact content of a component, recorded so that a later copy is checked against it. |
| Advisory | A published notice of a defect or vulnerability in one or more revisions of a component. |
| Qualified revision | A revision of a dependency that the work's evidence, a hardware contract, or a process of fabrication or certification fixes, so that no other revision is admissible without new evidence. |"""),
        ("Notes", """The undivided draft that this standard replaces had dependencies selected with the human owner. That decision is not one LVL0 assigns to the human owner (STND.DRAFT.42), so STND.DEPS.1 makes it a decision record of the actor making the change, weighed on the three criteria of SIMPL.4 from stated evidence. Installing, updating, or removing a dependency is still an action that needs an authorization (PRIME.7); the project constitution template has the agent that drafts a constitution propose a standing authorization for it, bounded by sources, packages, and volume per change, so that routine dependency work proceeds unattended. A thinly supported dependency is not refused; its record states what happens after its support ends (STND.DEPS.2). The records that HDES.3, ML.3, HW.3, and AGENT.22 ask for serve as the decision records and the record of revisions where they hold the content this standard names.

The latest revision that its publisher marks as stable is the default at adoption, unless a qualified revision is fixed (STND.DEPS.3). Pinned revisions are reviewed at each release, at most every 12 months, and in the unit of work that changes one (STND.DEPS.4), the cadence that the custodian set for dependency review below LVL0; the last trigger narrows that of STND.DFLT.11, which reviews every direct dependency, to the pinned revision that the unit changes.

STND.DEPS.6 verifies every fetched component against a recorded digest: the publisher's, where the publisher publishes one, and otherwise the digest of the first fetch, so that a later fetch that differs is caught even when no publisher signs the component. Research retrieval brings no fetched component unless the work comes to depend on what it retrieved. STND.DEPS.7 checks advisories before each release, the point at which a vulnerable revision would reach relying parties, and records as unchecked each dependency for which no authorization covers the retrieval or no source publishes advisories, so that neither absence blocks the release or passes silently. Both rest on GUARD.17, against the supply-chain row of STND.THRT.2, and bind at every class; both are normally automatic. For a project whose constitution adopts this standard, they protect more than the default threat model of STND.DFLT.18; the consequence that warrants it is undetected compromise of a fetched component, and the constitution that cites this standard is the recorded decision (GOV.11).

The files that declare a project's packages and their lock files are, in most ecosystems, already the record of the packages they install; STND.DEPS.10 lets them serve as the dependency record when they carry the reason and license identity. Material copied into the work stays apart and carries a record of its origin beside it (STND.DEPS.11), so that its license and origin stay visible after the copy. The revision of each compiler, interpreter, synthesis tool, and process design kit is an input of each result it builds (STND.DEPS.8), which REPRO.1 and REPRO.2 already ask; the provision names those tools so that none is left out.

This standard names no set of dependencies. A set that served across projects is a knowledge entry of kind dependency set (STND.KNOW.2), held in the workbench until a knowledge base is designated (AGENT.30), and cited in a decision record.

Under STND.CLASS.10, every default provision applies from CSQ3; STND.DEPS.5 asks for something only where a contract of DSGN.5 exists, which STND.CLASS.10 asks from CSQ2. No default provision raises the floor (GOV.11)."""),
    ],
    provisions=[
        P(1, "Dependency selection criteria", "Selection", """
The decision record of each adoption, replacement, or removal of a dependency SHOULD weigh, against an owned implementation, each criterion of the table of this provision, from the evidence that its row gives (SIMPL.4, REPRO.7).

| Criterion | Evidence |
| --- | --- |
| Applicability | The part of the dependency that the work uses, and the part of the regime of use that its stated behavior covers |
| Active support | The dates of its recent revisions, its responses to reports of defects and vulnerabilities, and the number of people whom its record shows supporting it |
| Carrying cost | Its exposure of the work to compromise through its supply chain, its footprint on constrained targets, its expected life, the fit of its license terms to the work's use and distribution, and the readability of the work without it |
""", ["SIMPL.4", "REPRO.7"], defines=["selection-criteria"]),
        P(2, "Thinly supported dependencies", "Selection", """
Where the record of a dependency's revisions and responses shows at most one person supporting it, its decision record SHOULD state how the work continues after that support ends (SIMPL.4).
""", ["SIMPL.4"]),
        P(3, "Initial revision choice", "Revisions", """
Where the work fixes no qualified revision of a dependency, the revision that the work adopts SHOULD be the most recent one that its publisher marks as stable and that is consistent with the rest of the computational environment (REPRO.9).
""", ["REPRO.9"]),
        P(4, "Pinned revision review", "Revisions", """
At each release, at intervals of at most 12 months, inclusive, and in each unit of work that changes a pinned revision, each pinned revision SHOULD be reviewed (REPRO.9). Each review SHOULD record why each dependency that it leaves at its revision stays there (REPRO.7, REPRO.9).
""", ["REPRO.9", "REPRO.7"]),
        P(5, "Contract tests on update", "Revisions", """
Before a change of the pinned revision of a dependency is relied upon, the tests that verify the work's contract with that dependency SHOULD pass on the new revision (DSGN.5, VV.8).
""", ["DSGN.5", "VV.8"]),
        P(6, "Fetched component integrity", "Integrity", """
Before an actor uses a fetched component, it SHALL verify the component against the integrity digest recorded for it (GUARD.17). Where the publisher of a fetched component publishes an integrity digest, the digest recorded for the component SHALL be that one (GUARD.17). Where the publisher publishes none, the actor that first fetches the component SHALL record the digest of the component as fetched (GUARD.17).
""", ["GUARD.17"], mode="binding"),
        P(7, "Advisories before release", "Integrity", """
Before each release, the actor that prepares it SHALL check the published advisories of each pinned dependency for which an authorization in force covers the retrieval and a source publishes advisories (GUARD.17). That actor SHALL record each other pinned dependency as unchecked in the record of the release (GUARD.17, PRIME.2). Each advisory that applies to a pinned revision and to a feature that the work uses SHALL be recorded in defect tracking (GUARD.17, QA.4).
""", ["GUARD.17", "PRIME.2", "QA.4"], mode="binding"),
        P(8, "Toolchain revisions as inputs", "Records", """
The revision of each compiler, interpreter, synthesis tool, and process design kit that builds or runs the work SHALL be recorded as an input of each result it helps produce (REPRO.1, REPRO.2).
""", ["REPRO.1", "REPRO.2"]),
        P(9, "Development tool record", "Records", """
Each tool on which the development of the work depends and on whose output no result relies SHOULD be listed in the dependency record with its revision, license identity, and reason (REPRO.9).
""", ["REPRO.9"]),
        P(10, "Package files as record", "Records", """
Where the files that declare the work's packages, with their lock files, give each package's exact revision, reason, and license identity, those files MAY serve as the dependency record of the packages they install (REPRO.9).
""", ["REPRO.9"]),
        P(11, "Incorporated external material", "Records", """
Each piece of external code, data, or text that the work incorporates SHOULD be kept apart from the work's own material, with a record beside it of its origin, revision, and license identity (REPRO.9).
""", ["REPRO.9"]),
    ],
)

# ================================================================ STND.PROJ
PROJ_TABLE = """| Section | Content |
| --- | --- |
| Identity | The project's name, purpose, and non-goals (SIMPL.10); a reference to the governance that designates the human owner (PRIN.1); the collaborators, and the route by which external contributions are accepted (QA.7); the software that the human owner classifies as agents or as automation (GOV.51); the owner of each interface shared beyond the project (DSGN.6) |
| Classification | The value of each attribute that the selector table of an adopted profile gives; the profiles selected, and each profile applied by analogy with its analogue (GOV.24, GOV.29); the components that hold domain items of each selected profile, with the execution paths of each by hardware type; the consequence class (GOV.13); the proportionality judgment (GOV.11) |
| Work process | How each unit of work is planned, executed, reviewed, and audited (QA.2); the stopping rule (QA.3) |
| Defects | Where defects are recorded, how blocking defects are marked, and the schedule of tracked ones (QA.4) |
| Review and release | Who reviews, and the independence that each class requires (QA.7, QA.8); regeneration before reliance (QA.9); promotion (QA.11); the release decision and its gate (QA.10) |
| Correction | The mechanism of correction propagation (QA.13) |
| Incidents | The incident mechanism (QA.15) |
| Dependencies | The dependency management mechanism (REPRO.9) |
| Records | The locations of the decision record, provenance, environment captures, and the ledger; the retention of records and their formats (REPRO.12); the independent copy of irreplaceable data (REPRO.13) |
| Working notes | The location of the working-notes workspace (INTPR.5) |
| Workbench | The location of the workbench, under version control and apart from the working-notes workspace (AGENT.35, AGENT.36) |
| Knowledge base | The knowledge base designated for the work, or the statement that none is designated (AGENT.30) |
| Secret store | The location of the store of AGENT.44, outside version control, every record, and the working-notes workspace; the accounts that read it; its protection under the threat model; and that no archive, backup, or transfer of the work carries it; or the statement that the work keeps none |
| Access descriptors | The vocabulary of access descriptors (AGENT.23), or the statement that the work makes no network access |
| Threat model | The threat model (GUARD.16) |
| Reserved actions | The reserved-action register and its exempt classes (GUARD.4, GUARD.7) |
| Authorizations | The authorization mechanism (GUARD.10); each standing authorization in force, with its scope and duration (GUARD.11); the authorization for read-only research retrieval, with its purpose, its scope, and its bounds on items and volume per research effort, or the statement that none is granted (GUARD.8, GUARD.13); the discipline for the operating cost of agents, or the statement that none is set (GUARD.14) |
| Agent instructions | The agent instructions, and the form of the findings and justification statement (GOV.48, PRIME.14) |
| Configuration | The configuration, unalterable by an agent, that settles the tier of an agent's actions, or the statement that none does (GUARD.2); the other configuration of agents and tools, and who changes it (GOV.49) |
| Architecture | The recorded dependency structure of the components (DSGN.7) |
| Physical hardware | Where the work drives physical hardware, the hazard analysis, the safe state, and the safe range of actuation (PRIME.13) |
| Exceptions | The logs of waivers (GOV.44), exceptions (PRIN.10), dissent (REPRO.8), and rulings (GOV.3) |"""

PROJ_REFS = ["SIMPL.10", "PRIN.1", "QA.7", "GOV.51", "DSGN.6", "GOV.24",
             "GOV.29", "GOV.13", "QA.2", "QA.3", "QA.4", "QA.8",
             "QA.9", "QA.11", "QA.10", "QA.13", "QA.15", "REPRO.9",
             "REPRO.12", "REPRO.13", "INTPR.5", "AGENT.35", "AGENT.36",
             "AGENT.30", "AGENT.44", "AGENT.23", "GUARD.16", "GUARD.4",
             "GUARD.7", "GUARD.10", "GUARD.11", "GUARD.8", "GUARD.13",
             "GUARD.14", "GOV.48", "PRIME.14", "GUARD.2", "GOV.49", "DSGN.7",
             "PRIME.13", "GOV.44", "PRIN.10", "REPRO.8", "GOV.3",
             "STND.CLASS.10"]

PROJ = dict(
    id="STND.PROJ", title="Project constitution template",
    instantiates=["GOV.20", "GOV.21"],
    sections=[
        ("Purpose and scope", """This standard fixes what a project constitution holds (GOV.20, GOV.21): one section for each mechanism that LVL0 requires of every project, the classification and its judgments, the places where the work's notes, workbench, knowledge, and secrets are kept, the authorizations in force, and, for work that drives physical hardware, its safety instruments. A filled copy is a LVL3 instrument that the project's human owner adopts (GOV.41). A section states its content in full or adopts by citation the provisions of an adopted LVL2 standard (STND.PROJ.2), so that a project takes the defaults, the agent instructions, the dependency policy, and the threat-model template without restating them, and a section whose content the project's class does not yet ask for says so (STND.PROJ.1). STND.PROJ.3 recommends the standing authorizations that let routine work run unattended, proposed once at the project's start (STND.DRAFT.42). STND.PROJ.1 to STND.PROJ.3 are binding, because each instantiates GOV or GUARD, which the floor holds (GOV.10); STND.PROJ.3 is a recommendation within a binding provision. STND.PROJ.4, on the form of the files, is a default (GOV.19). The standard names no tool or method (GOV.18)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """

| Term | Definition |
| --- | --- |
| Section | A part of a project constitution under one heading, named by a row of the table of STND.PROJ.1. |
| Project template | The directory `_PROJECT/NAME` of the governance corpus, which holds the document file of a project constitution and one example file of each kind of project instrument. |"""),
        ("Notes", """The sections follow GOV.21 and the conforming work that AGENT left to this template: the workbench, the knowledge base, the store of non-credential secrets, the vocabulary of access descriptors, and the authorization for read-only research retrieval. A section that adopts a provision of STND.DFLT by citation adopts its content as the project's own; STND.DFLT.1 still keeps the defaults themselves from applying once a constitution exists. A standing authorization for research retrieval that the human owner has granted is entered once in each covered project's own ledger and cited in the section Authorizations; its bounds are the human owner's, at LVL3 (GOV.18).

The sections ask for what each mechanism is, not for a plan of the work. Every row other than its parts that STND.CLASS.10 defers is required at every class, because GOV.21 requires each mechanism of every project; a part that STND.CLASS.10 applies only from a class more severe than the project's, such as regeneration before reliance (QA.9) below CSQ1, is stated as not applying, so the template raises no floor (GOV.11). A verification and validation plan, budgets, and the other content that a profile asks for are recorded where that profile asks. The project template holds the files for authorizations, axioms, hazards, safe ranges of actuation, rulings, waivers, and the reserved-action register, so that each such instrument is a file the ledger pins (STND.PROJ.4).

The standing authorizations of STND.PROJ.3 are those the custodian found needed for unattended routine work, each scoped so that it reaches no reserved action. Removal of a dependency is covered only where reinstalling its pinned revision from a named source restores it, so that the removal is recoverable (GUARD.5). Machine-local settings are covered only where the prior value is recorded and restorable, and never for the store of secrets, the configuration that settles an agent's tier, a setting that enables a security or integrity check, a setting that selects a source or destination of network access or runs a program without a request, or a conventional location of secrets or credentials, so that no setting widens another authorization. Commits to a private remote repository never rewrite or delete history, a branch, or a tag, never reach a release branch or a branch whose update publishes or deploys, and lapse when the repository no longer meets the human owner's record. Every release, publication, and other remote write whose effect is irrevocable stays with the human owner or is authorized per action (PRIME.6, GUARD.5, GUARD.6, GUARD.11); no standing authorization covers one. A request made under the research authorization carries no secret (AGENT.43)."""),
    ],
    provisions=[
        P(1, "Constitution sections", "Contents",
          "A project constitution SHALL hold one section for each row of the table of this provision, stating the content that its row gives (GOV.20, GOV.21). Where STND.CLASS.10 applies the obligation that a part of a row's content instantiates only from a class more severe than the project's, the section MAY state that the part does not apply (GOV.11).\n\n" + PROJ_TABLE,
          ["GOV.20", "GOV.21", "GOV.11"], refs=PROJ_REFS, mode="binding",
          defines=["constitution-sections"]),
        P(2, "Sections adopted by citation", "Contents", """
A section MAY state its content by citing each provision of an adopted LVL2 standard that it adopts as the project's own (GOV.21).
""", ["GOV.21"], mode="binding"),
        P(3, "Proposed standing authorizations", "Authorizations", """
An agent that drafts a project constitution SHOULD propose to the human owner, in its section Authorizations, each standing authorization of the table of this provision, with its scope and duration (GUARD.10, GUARD.11).

| Class of actions | Scope |
| --- | --- |
| Installing, updating, and removing dependencies | Only from the sources that the authorization names, within the number of packages and the volume per change that it states, each verified under STND.DEPS.6 and installed without elevated privilege, and each removal restorable by reinstalling its pinned revision from a named source |
| Changing machine-local settings | Within the provisioned privilege, for a setting whose prior value is recorded and restorable, other than the store of AGENT.44, a configuration that settles the tier of an agent's actions, a setting that enables a check of security or integrity, a setting that selects a source or destination of network access, a setting that runs a program without a request, and a location that holds secrets or credentials by convention |
| Read-only research retrieval | For a stated purpose, from sources of a stated kind, within bounds on items and volume per research effort |
| Adding commits to a private remote repository | Where the human owner records that repository as part of the provisioned environment and as readable only by those whom the threat model trusts, to branches other than release branches and branches whose update publishes or deploys, without rewriting or deleting history, a branch, or a tag, and lapsing when the repository no longer meets that record |
""", ["GUARD.10", "GUARD.11"], refs=["STND.DEPS.6", "AGENT.44"], mode="binding",
          defines=["proposed-authorizations"]),
        P(4, "Constitution files", "Form", """
A project constitution SHOULD be kept as a copy of the project template, with its sections in the document file and the reserved-action register and each authorization, axiom, hazard, safe range of actuation, ruling, and waiver in an instrument file of its kind (REPRO.12, INTPR.12).
""", ["REPRO.12", "INTPR.12"]),
    ],
)

NEW_DOCS = [CODE, THRT, KNOW, DEPS, PROJ]

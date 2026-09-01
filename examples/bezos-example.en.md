# The `bezos` agent by example: "three weeks debating the output format"

> **The agent.** `bezos` classifies a decision before choosing its speed:
> is the door two-way (reversible) or one-way, and does the process match
> the door's type. Reversibility is proven by a rollback mechanism, not by
> the word "rollback"; the signature move is narrowing the irreversible by
> design: a flag, a canary, a backup. It catches month-long debates over
> the hour-reversible and the irreversible done on the fly. Input — the
> decision and the process deciding it. Full definition:
> [`agents/bezos.md`](../agents/bezos.md).

A model run on the `http2md` project — the "URL → markdown" pipeline.
Four decisions, four doors, four different verdicts.

## Decision 1: changing the markdown output format — three weeks of debate

The team is in week three of arguing about a new heading format; the
format is already implemented behind the `--format-v2` flag. The thread
holds 4 people and 40 messages.

```
DOOR TEST
  rollback mechanism — turning off the --format-v2 flag (cli.py:88)
  rollback cost      — one routine action; the evidence is the
                       mechanism itself
  rollback right     — ours
  residue            — not found: searched issues, README, the PR thread

MATCHING
  process cost — 4 people × 3 weeks of thread (PR #61, 40 messages)
  vs rollback cost — flipping a flag; the debate costs orders of
  magnitude more than the rollback

VERDICT — a two-way door — decide fast: the CLI owner, alone.
  Defect one: the debate (3 weeks × 4 people) costs more than the
  rollback (one flag). Speed is an asset too, and its loss is
  irreversible.

  the report's most expensive claim — there is no residue
  how it is refuted — a user complaint about the format change in
    issues after enabling: if it appears, the flag goes off and the
    debate resumes — now with evidence
```

## Decision 2: "rewrite the cache to SQLite, we'll roll back if needed"

```
DOOR TEST
  rollback mechanism — not named: "we'll roll back" in the thread
                       (PR #64) is not a mechanism
  rollback cost      — unknown
  ...

VERDICT — false two-wayness — stop: reversibility is claimed, the test
  fails (no mechanism named). Until presented, the door counts as
  one-way and the process as full. Program — the cheapest presentation
  first: name the mechanism (is the file cache regenerable? a backup?),
  then the right, then a rollback run on a stage.
```

Repeat entry: "the cache regenerates from scratch in minutes; rollback
is deleting the SQLite file and flipping the flag back" →
reclassification → **a two-way door — decide fast**. The word
"rollback" became a mechanism — and only then did it buy speed.

## Decision 3: "enable the new parser for all users"

The parser was rewritten; the proposal is to enable it for everyone at
once — "discussed at standup."

```
DOOR TEST
  rollback mechanism — a revert exists, but residue: pages converted
  wrong during the incident have already reached users — unreturnable

NARROWING
  canary: a flag + 5% of users for a week; cost — a day of work;
  the core (full rollout) remains, but is decided after the canary
  with evidence in hand

VERDICT — the door narrows — here is the move: a 5% canary (a day of
  work) plus the full process for the core is cheaper than the full
  process for the whole. Decide the shell (canary) fast; the core
  (rollout to all) — after a week of evidence.
```

## Decision 4: "publish the package to PyPI — settled in chat one evening"

```
DOOR TEST
  rollback mechanism — a publication cannot be recalled: the name is
  taken forever; the rollback right belongs to PyPI, not us; residue —
  the name, the version scheme, whoever starts depending on it

VERDICT — a one-way door — full process. Irreversible: the package
  name, the versioning scheme, emerging dependents. Defect two:
  "settled in chat one evening" — a light process on a one-way door.
  What the process lacks: a name-collision check, a versioning scheme,
  a run on test.pypi.org (which is also the narrowing: a rehearsal
  without the core).
```

## Why it pays

| | The usual process | bezos |
|---|---|---|
| How speed is chosen | one speed for everything: some route all through RFCs, some settle all in chat | classifies the door first, then picks the speed |
| "We'll roll back" | taken at its word | a mechanism, or a stop |
| Verdict | "let's discuss more" / "ship it" | the flag — decide alone today; PyPI — turn on every light |

Three weeks on a reversible flag and one evening on an eternal package
name — the same team commits both defects at once. Doors are classified
before choosing the speed, not after.

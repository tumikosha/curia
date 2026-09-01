# Agent `larrey` by example: "should we rewrite the parser in Rust?"

> **What this agent is.** `larrey` is review triage, named after
> Napoleon's surgeon who invented sorting the wounded by the profile
> of the wound, not by rank. It neither judges the artifact nor
> launches agents — it assigns: a minimal reviewer roster (≤4), each
> one's input, the order, the merge via `review-arbiter`; the caller
> executes. Catches "everyone on everything," "the wrong
> specialist," and "a choir with no merge." Team protocol —
> [`TEAM.md`](../TEAM.md). Full definition:
> [`agents/larrey.md`](../agents/larrey.md).

A model run on the `http2md` project — a "URL → markdown" pipeline.
Three inputs.

## Run 1: phase A, capacity cut

Input: "we want to rewrite the parser in Rust: 5x faster, we'll
throw out the Python code; a month of work. Is it worth doing?"

```
INPUT
  artifact/intent — rewriting the parser in Rust
  caller's question — "is it worth it" → phase A
  repeat entry — no

ROSTER — round 1 (parallel, isolated; ≤4)
  hamming — holder of the question "is it worth it" (exempt from
    the capacity contest) — input: the intent + the field's list of
    important problems, if present
  munger  — phase A base — input: the goal with the criterion
    "5x faster"
  fermi   — trigger: the numbers "5x" and "a month" — input: the
    numbers and what to measure them against
  chesterton — trigger: "we'll throw out the Python code" —
    deletions — input: what is deleted and who leans on it
  substitutions — none
  cut — suntzu: capacity cut — limit 4, position 1 in the
    phase-A cut order

MERGE
  review-arbiter — after all reports

ROUND 2  (≤2; there is no round 3)
  execute: munger's probabilistic candidates → premortem;
  fermi's "measurement unavailable" → suntzu
  remainder — "uncovered — a separate call at the owner's decision"

  the report's most expensive claim — phase A per the question
  how to refute it — an input line showing work already started
    (then phase B and a different roster)
```

## Run 2: a jurisdictional question with a trigger

Input: "we're switching off legacy config support next release —
which door is this?"

The question matches `bezos`'s jurisdiction — but the input carries
a detectable trigger: switching off is a deletion someone may lean
on → `chesterton`. Triggers beat phrasing: the input is not solo.

```
ROSTER — bezos (question holder, first) + chesterton (trigger:
  deletion); the phase base is not added — the question is narrow
MERGE — review-arbiter: there are two reports
```

## Run 3: phase undeterminable

Input: "here's the cache-migration plan doc" — no question; the doc
doesn't show whether work has started.

```
VERDICT — question asked — roster deferred:
  "is the work not started, in progress, or presented as done?"
```

The caller's answer "not started" is a legal repeat entry: phase A,
triage continues. No answer on the second pass either — presumption
C, marked "confirm."

## Why this is useful

| | Without triage | larrey |
|---|---|---|
| Roster | "call everyone" — 19 reports | ≤4 specialists, cuts named |
| The caller's question | can drown in the choir | holder exempt — always judged |
| Convenient phrasing | "it's just a door question" | triggers beat phrasing |
| Report conflicts | the caller untangles them | review-arbiter — one verdict |

Sorting by the wound, not by rank: every input meets exactly the
questions it touches, the judges work silently and in parallel, and
the caller gets one verdict — not a choir.

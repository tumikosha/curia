# Agent `munger` by example: "switch to v2 and delete v1"

> **What this agent is.** `munger` is Jacobi's and Munger's inversion:
> instead of "how do we succeed," ask "how do we guarantee failure" —
> then check the list against the artifact. A killer is only legal with
> a guarantee mechanism: a causal chain that makes the success
> criterion unreachable, with no "if we're unlucky" link; probabilistic
> scenarios go to the premortem. Catches polishing the road to success
> while a road to death stays open, and killers "excluded" by intention
> instead of mechanism. Input — a goal with a success criterion,
> ideally an artifact. Full definition:
> [`agents/munger.md`](../agents/munger.md).

A model run on the `http2md` project — a "URL → markdown" pipeline.
One plan, three runs.

## The situation

The plan: "switch the pipeline to parser v2 and delete v1 by the end
of the month." Success criterion: successful-conversion rate on the
reference corpus at least 97%, directory `parsers/v1/` deleted. The
plan polishes the road to success: v2 speed benchmarks, a new CLI
flag, a beautiful changelog.

## Run 1

```
INPUT
  goal / success criterion — stated: rate ≥97% on the reference
    corpus, v1 deleted
  artifact — plan-v2-cutover.md
  constraints — deadline (end of month), irreversibility of deleting v1

ANTI-GOAL
  corpus rate not demonstrated or below 97% — or v1 still there

KILLERS  (2 survived)
  killer 1 — cutover with table support unimplemented
    guarantee mechanism — the plan itself says: "v2 doesn't support
      tables yet (TODO)"; 30% of the reference corpus are pages with
      tables (corpus/stats.json). Rate ceiling = 70% < 97% — one
      multiplication on input constants, no luck link: the "rate ≥97%"
      component is unreachable while tables don't work
    candidate source — criterion component 1 + the plan's admission
      against itself
    status — being committed: the plan schedules cutover for week 2,
      table support "after stabilization"
  killer 2 — deleting v1 with no rate measurement presented
    guarantee mechanism — the criterion demands a proven rate; the
      plan has no corpus-measurement step at all — the "rate ≥97%"
      component cannot be demonstrated: unprovable doesn't count as
      achieved
    candidate source — criterion component 1
    status — unaddressed

DISCARDED CANDIDATES
  "v1 deletion is irreversible, no rollback" — probabilistic: the
    criterion doesn't require surviving a failure, the chain carries
    "if v2 breaks" — premortem; the door is one-way — bezos clearance
  "we won't fit in a month" — numeric: ranges and folding — proof
    belongs to fermi

VERDICT — failure guaranteed — killer 1 is being committed: cutover
  is scheduled before table support, the criterion is unreachable
  right now; benchmarks and changelog are polishing the road to
  success while a road to death stays open. Minimal exclusion: route
  pages with <table> to v1 until the TODO closes — or drop tables
  from the criterion by owner's decision. For killer 2 the cheapest
  mechanism: a measurement step before deletion.

  the report's most expensive claim — 30% of the corpus has tables
  how to refute it — recount corpus/stats.json with one command
```

## Run 2: the plan amended — "we'll add a CI gate"

The owner amended the plan: "before deleting v1, CI runs the corpus;
rate <97% blocks deletion" and "pages with tables are routed to v1."

```
KILLERS
  killer 1 — status: claimed — confirm with an artifact outside the
    plan's text: a line of the plan under review is not a mechanism's
    artifact
  killer 2 — status: claimed — confirm: the CI gate is a plan item,
    the config doesn't exist yet

VERDICT — roads to death closed — CONDITIONAL: both exclusions are
  lines of the plan itself; present .ci/corpus-gate.yml and the
  routing rule in code. A plan does not certify itself. A closed loss
  promises no win — "is v2 worth it at all" is not decided here
  (hamming/suntzu).
```

A week later — a repeat entry: the gate config and the routing in
code, `file:line`. Statuses "excluded," the verdict unconditional.

## Run 3: a goal, no plan yet

"We want OCR for PDF pages; criterion — 90% of PDFs yield readable
markdown. No plan yet — where do we die?"

```
VERDICT — list without a check — killers as prohibitions:
  - accepting "readable" with no binary test — the component is
    unreachable as proof: a readability reference is needed upfront
  - measuring the 90% on PDFs hand-picked to suit OCR — sampling echo
  - switching off the text extractor before measuring OCR on its
    class of pages
  bring the plan — the check is a repeat entry
```

## Why this is useful

| | The plan's self-assessment | munger |
|---|---|---|
| "v2 is faster and cleaner" | benchmarks, changelog | polishing while a road to death is open |
| Tables | "TODO, after stabilization" | admission against itself: ceiling 70% < 97% |
| "We'll add a CI gate" | plan item = protection | a plan's line is not an artifact: conditional |
| Rollback risks | "we'll be careful" | probabilistic — premortem; the door — bezos |

The direct question collects wishes; the inverted one collects
checkable prohibitions. Failure arrives whole, and closing it is
cheaper than buying percentage points of success: where we'd die, we
don't go — everything else may stay bold.

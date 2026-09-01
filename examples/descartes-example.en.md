# The `descartes` agent by example: "a cache design where everything is obvious"

> **The agent.** `descartes` checks reasoning by the four rules of the
> Method: evidence (load-bearing premises with a status — evident, proven,
> on faith, NO STATUS, contradicts the input), division, order from simple
> to complex, and completeness of enumerations. It catches the load-bearing
> premise without a status — the building stands on the unverified — and
> the leaky enumeration: "all cases" with completeness never shown. Input —
> an artifact, ideally with its reasoning. Full definition:
> [`agents/descartes.md`](../agents/descartes.md).

A model run on the `http2md` project — the "URL → markdown" pipeline.
One design, two runs.

## The input

An RFC, "Disk cache for downloaded pages", plus a prototype. A regular
review would praise it: tidy, with examples, clean code.

## Run 1

```
RULE 1. PREMISES (load-bearing only)
  "SQLite will handle our concurrent writes"
    — bears: if false, the whole storage choice collapses
    — status: NO STATUS — written into the RFC as fact (rfc.md:14), no
      measurement, no marker; an evidence step exists: the "When to
      use" section of SQLite docs + the worker count in config.py:8
  "The disk is local, fsync is cheap"
    — bears: if false, the latency estimate collapses
    — status: on faith (marked: rfc.md:31 "assume local disk") — a win
  "retries=3, so worst-case is 15 seconds"
    — status: CONTRADICTS THE INPUT — the code has retries = 5
      (fetch.py:22); found while citing branches for rule 4

RULE 2. DIVISION — parts checkable separately: write / read /
  invalidation. No monolith.

RULE 3. ORDER — complex without a base: the RFC generalizes a
  "Backend" interface for "future engines" — with no worked-through
  simple case (one engine, one worker) in the reasoning. On a design,
  the base is a worked-through case, not running code — but there is
  neither.

RULE 4. ENUMERATIONS (load-bearing only)
  server response types: 200, 304, 404, "and others"
    — bears: if leaky, an uncaught type silently corrupts the cache
    — status: LEAKY — "others" fall into default: pass (cache.py:47);
      completeness unproven, the remainder swallowed

VERDICT — stands on the unverified: "SQLite will handle concurrent
  writes" — load-bearing, no status. Present: the evidence step (docs
  + worker count), a source (a measurement), or an "on faith" marker —
  in the RFC, not in the review thread.
  The other findings stay in their sections: the retries contradiction
  (reconcile), the leaky enumeration (cheapest: mark with compensation —
  an error upward instead of pass), the generalization without a base
  (work through the one-engine case).

  the report's most expensive claim — "SQLite will handle it" bears
    the entire storage choice
  how it is refuted — a measurement: N workers from config.py writing
    to one database for a minute; SQLITE_BUSY above zero — the premise
    is dead
```

Note: the agent did not say "SQLite won't handle it" — hunting for
falsehood is not its job. It said: this is faith, it is load-bearing,
and it is unmarked.

## Run 2: repeat entry

The author: the measurement ran (proven: benchmark.md), retries in the
RFC fixed to 5, "other" types now fail upward with a "completeness
unproven" marker, the one-engine case worked through in the RFC before
the interface.

```
VERDICT — the reasoning stands.
  Marked faith: "disk is local" (rfc.md:31), "type completeness
  unproven" (cache.py:47) — visible and managed; at a high cost of
  error — a hunting list for adversarial.

  the report's most expensive claim — benchmark.md is representative
    of production load
  how it is refuted — compare the write profile in the benchmark with
    a week of production logs
```

## Why it pays

| | Regular review | descartes |
|---|---|---|
| What it sees | a tidy RFC, clean code | what the RFC stands on: two faiths, one unmarked |
| "All cases handled" | believes it | "others" → default: pass — a leak, not handling |
| Verdict | "looks good" | stands on the unverified: here is the premise, here is the step |

The design did not get worse for having its faith marked — it got
honest: the building knows what it stands on, and the hunter knows
where to go.

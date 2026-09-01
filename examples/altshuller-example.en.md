# The `altshuller` agent by example: "let's halve the parallelism"

> **The agent.** `altshuller` runs the core of ARIZ: function over
> mechanism, the ideal final result as a ruler (the function performs, the
> mechanism is gone), a contradiction "improving A worsens B" with
> independent criteria, and its resolution by separation along a
> coordinate — in time, in space, by condition, between system and parts.
> It catches compromise instead of resolution (a criterion bought off, the
> conflict alive) and symptomatic solutions. Input — a pain/task, ideally
> with a solution. Full definition:
> [`agents/altshuller.md`](../agents/altshuller.md).

A model run on the `http2md` project — the "URL → markdown" pipeline.
One contradiction, three runs.

## The situation

A batch run of 500 URLs with 16 workers: fast, but servers ban the
frequent requests — the run fails. The PR proposal: "drop parallelism
to 4 — speed is tolerable and bans are rarer." A regular review would
approve: balanced, careful.

## Run 1: a compromise

```
FUNCTION — a 500-URL batch downloads fast and without bans
IFR — servers themselves serve pages at the maximum rate they allow;
  no throttling mechanism exists

CONTRADICTION (the directed link holds: more parallelism — faster runs
  AND more bans, at any thresholds)
  requirement A — run ≤ 10 min — criterion: the batch-mode SLO
                  (README:22) — source independent of the solution
  requirement B — zero bans per run — criterion: ticket #83 "the run
                  fails" — source independent

SOLUTION ANALYSIS (workers 16 → 4)
  requirement A — PARTIAL: the run takes ~25 min, SLO violated
                  (measurement in the PR)
  requirement B — whole: no bans on the test run
  → both live in one coordinate (global parallelism), A was bought

VERDICT — compromise — the conflict is alive: requirement A is partial.
  Coordinate sweep (mine, in this same report):
  - in space: parallelize PER DOMAIN — 16 workers, but ≤1 concurrent
    request per domain; bans are counted by the domain, speed by the
    batch; APPLICABLE, yields both whole
  - in time: a night run — bans do not vanish, DOES NOT SOLVE
  - by condition: slow only for banning domains — applicable as a
    complement (adaptive backoff on 429)
  - system-parts: each worker polite, the pool aggressive — the
    per-domain scheme in other words
  Program for the caller: accept the coordinate, price it out, or
  present the decider's choice.

  the report's most expensive claim — it is the domain that bans, not
    the pipeline's total traffic volume
  how it is refuted — a 16-worker run over 16 distinct domains: bans
    appear → volume bans, the coordinate will not work
```

The compromise is not branded bare-handed: the coordinate sweep is
attached, and the caller has three exits.

## Run 2: repeat entry — the separation adopted

Implemented: 16 workers, a per-domain queue, ≤1 request per domain.

```
SOLUTION ANALYSIS
  requirement A — whole: the run takes 8 min (measured) — SLO met
  requirement B — whole: zero bans across three runs
  coordinates — A over the whole batch, B on each domain: different

THE SWEEP OF FIVE (what the move itself worsened)
  resource — whole: the same 16 workers
  complexity — whole: the domain queue is 30 lines, operations
    unchanged
  latency — whole (SLO met), freshness — whole, security — whole

VERDICT — the contradiction is resolved — the move: separation in
  space (per domain). Both whole.
  Distance to the IFR: mechanism added — the domain queue; the function
  is achievable without it — if servers send Retry-After, the queue
  becomes honest header-waiting (closer to "the server states its own
  rate").
```

## Run 3: a neighboring input — "dissolved at the given thresholds"

The same pipeline, now the cache: TTL=60s, SLO p99<100ms (README) and
freshness ≤60s (ticket #91). The directed link holds, but both
independent criteria are met head-on.

```
VERDICT — dissolved at the given thresholds — no separation needed.
  Review trigger: a freshness requirement tighter than 60s brings the
  conflict back — then the coordinates from the sweep: by condition
  (freshness for logged-in users only — if the ticket narrows scope).
```

But had there been no SLO, with criteria recoverable only from the
cache's own TTL constant — that is an echo, not a criterion: the
verdict would be "symptomatic solution — name independent criteria",
not "dissolved."

## Why it pays

| | Regular review | altshuller |
|---|---|---|
| "Halve it" | "balanced, approved" | a compromise: the SLO bought off, the conflict will return |
| What it offers | accept or reject | a coordinate where both requirements live whole |
| The ruler | "better than before" | distance to the IFR: what was added and what it can do without |

A conflict bought with a compromise returns with growth; a conflict
separated along coordinates is closed — and the solution gains a ruler
whose zero is "the system does it itself."

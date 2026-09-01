# The `boyd` agent by example: "we deploy every day — we're fast"

> **The agent.** `boyd` runs the OODA loop: observe → orient → decide →
> act. It checks whether the loop is closed (every action returns as an
> observation of its result, and someone actually reads the channel) and
> whether the full turn is shorter than the environment's tempo. The
> better decision loses to the shorter cycle. It catches polishing
> decisions while the cycle outlasts the tempo, broken loops, and frozen
> orientation. Input — the loop or material to reconstruct it, ideally
> with the environment's tempo. Full definition:
> [`agents/boyd.md`](../agents/boyd.md).

A model run on the `http2md` project — the "URL → markdown" pipeline.
One loop, three runs.

## The situation

The team is proud: "we deploy the parser daily." The loop is conversion
quality: users report broken pages, the team patches the parser, ships,
moves on.

## Run 1

```
INPUT
  loop — reconstructed from: issues, git log, grafana/
  environment tempo — reconstructed: the changelog of the corpus's
    top-20 domains — source markup changes every [2–6] weeks
    (external source)
  action classes — parser deploys, reference-corpus edits

THE LOOP
  observe — complaints in issues (a channel exists); a broken-page-rate
    dashboard EXISTS (grafana/parse-rate.json)
  orient — BROKEN: no trace of anyone reading the dashboard — no synch
    review, no picture update, no alert reaction in 4 months (git log
    docs/, synch notes); a channel without a reader is an archive
  decide — the lead, within a day (claimed — to confirm)
  act — daily deploys (git log)
  turn — full, until the observation returns: complaint → fix →
    deploy → ...first reaction to the metric — NEVER CLOSES

VERDICT — the loop is broken — close it: orientation does not read
  its own dashboard; daily deploys do not make the loop fast — action
  without an absorbed result is half a turn.
  Program: a Friday parse-rate review over top domains, 15 minutes;
  an alert on the rate dropping below 95%.

  the report's most expensive claim — nobody reads the dashboard
  how it is refuted — one reading trace in 4 months: a picture update
    or an alert reaction with a date
```

"We deploy daily" turned out to be the speed of action, not of the
loop: the turn is measured until the observation returns — and it
never did.

## Run 2: the channel closed — now the tempo

The Friday review is in place. Repeat entry a month later.

```
THE LOOP
  turn — full: complaint/metric → review (up to 5 days waiting for
    Friday) → fix → deploy → metric into the next review =
    [7–12] days (dates of four turns)

ENVIRONMENT TEMPO
  source markup — [2–6] weeks (changelog, external)

COMPARISON — the [7–12]-day turn is shorter than the [14–42]-day
  tempo, but the ranges are close at the tempo's lower bound

VERDICT — hold the tempo — headroom ×1.2–6; the narrow stage for the
  future: waiting for Friday (up to 5 of the 7–12 days — orientation
  on a schedule, not on a signal). The "parser deploy" class is
  reversible: a canary run over 100 pages + revert — the mechanism is
  named, the verdict is unconditional.

  the report's most expensive claim — the [2–6]-week source tempo is
    representative: the top-20 changelog covers the corpus
  how it is refuted — tail drift: the broken-page share outside the
    top-20 over the same month
```

## Run 3: a neighboring input — not ours

"Let's speed up corpus edits: hire a second editor" — a change with
the question "is the work aimed right" → redirect to `goldratt`: this
loop's narrow stage is waiting for Friday, not the editor's hands, and
his five steps will test that as the constraint.

## Why it pays

| | The team's self-image | boyd |
|---|---|---|
| "We're fast" | daily deploys | the turn never closed: action without absorption |
| Metrics | "we have a dashboard" | a channel without a reader is an archive |
| Speed | polish the decisions | cut the Friday wait: orientation on signal |

The loop's speed is not the speed of action but of the full turn — up
to the moment the result comes back and changes the picture. Everything
else is running in place with a brisk step.

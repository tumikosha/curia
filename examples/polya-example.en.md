# The `polya` agent by example: "duplicates found, work done"

> **The agent.** `polya` checks how a problem was worked, by the four
> phases of "How to Solve It": understand the problem → devise a plan →
> carry it out → look back. A phase counts as done if its trace is
> recoverable from the artifact. It catches solving by assault (a local
> miss, unused data) and the skipped look-back — work declared "done"
> with the result never checked a second way. Input — the problem as
> stated and the artifact: a plan, work in progress, or a finished
> solution. Full definition: [`agents/polya.md`](../agents/polya.md).

A model run on the `http2md` project — the "URL → markdown" pipeline.
One problem, three runs.

## The problem

"The reference corpus has grown duplicates: the same content under
different URLs. Find all duplicate groups. Given: a list of URLs, each
with its server ETag and the content-hash of the downloaded HTML."

## Run 1: a finished solution, by assault

The solution compares pages by content-hash; the test is a snapshot of
the found groups.

```
PHASE 1. UNDERSTAND
  unknown   — the duplicate groups; the artifact answers this
  data      — URL, ETag, content-hash; ETag is USED NOWHERE
              (grep over the solution: no mentions)
  condition — sufficiency unchecked

VERDICT — return to phase 1 — present: where the ETag datum goes.
  An unused datum is Polya's marker: either the condition is redundant
  or it was not understood. Ask the problem-setter why ETag is given.

  the report's most expensive claim — ETag is redundant
  how it is refuted — one known mirror pair in the corpus: their
    content-hashes differ (a timestamp in the footer), their ETags
    match — hash comparison misses them; ETag was the key
```

The refutation fired: hashes differ because of a footer timestamp.
ETag was not redundant — the problem was half-understood.

## Run 2: the solution reworked — but no look-back

Duplicates are now grouped by ETag with a fallback to a normalized hash
(the footer is stripped). The test — a snapshot of the group list.

```
PHASE 1 — all data used, the artifact answers what was asked
PHASE 2 — the plan is separable: normalize → group → merge
          (module structure + commit message "two-pass dedup")
PHASE 3 — the normalize step is unit-tested; merge — accepted
          unchecked (marked)

PHASE 4. LOOK BACK
  (a) — the snapshot test: expected groups were recorded from the
        solution's own output — the value's origin is unrecoverable,
        independence "unknown", not credited

VERDICT — the work is not finished — close the look-back.
  Program: the cheapest independent check — the known mirror pair from
  run 1 (the answer known from another source: they are documented
  mirrors) must land in one group; plus the degenerate case — a corpus
  with no duplicates yields zero groups.
```

A snapshot recorded from the solution's own output is not a check: it
would freeze a bug just as happily. Independence is a trace with a
source, too.

## Run 3: repeat entry

Both checks ran: the mirrors share a group, the empty corpus yields
zero groups.

```
VERDICT — the cycle is closed.
  Look-back: (a) mirrors and the degenerate case — independent of the
  solution's path; (b) simpler: grouping by sort instead of pairwise
  comparison — O(n log n), adopted; (c) transfer: footer normalization
  will serve the parser — moved to a shared module (normalize.py).
  The merge step remains unchecked — marked.

  the report's most expensive claim — normalization removes ALL noise
    between mirrors
  how it is refuted — a third mirror pair with an ad block: run it —
    do the groups diverge?
```

The look-back produced value, not a checkbox: the method moved to a
shared module, the complexity dropped, and the result gained an
independent leg to stand on.

## Why it pays

| | Regular review | polya |
|---|---|---|
| What it sees | the solution's code: clean, test green | ETag unused; the snapshot recorded from the solution's own output |
| "Work is done" | accepts | not finished until the result is checked another way |
| After solving | next task | the method extracted and transferred |

The first "done" answered half the problem; the second rested on a test
that would have frozen a bug. The real "done" appeared after the
look-back — the phase almost everyone skips almost always.

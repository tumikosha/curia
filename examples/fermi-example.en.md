# The `fermi` agent by example: "we'll run it all overnight"

> **The agent.** `fermi` estimates orders of magnitude before work
> starts: decompose the promise into 3–7 factors, estimate each as a
> range with grounds (measurement, analog, anchor, ×10 convention), fold
> the bounds — product, sum, or max by whether contributions share the
> budget — and compare against the budget with the quantity's direction
> in mind. It cheaply kills projects whose arithmetic does not add up;
> it catches numbers nobody ever multiplied and false precision. Input —
> the plan and its numbers. Full definition:
> [`agents/fermi.md`](../agents/fermi.md).

A model run on the `http2md` project — the "URL → markdown" pipeline.
Two plans, three verdicts.

## Plan 1: "we'll reconvert the corpus overnight"

"Reconvert the whole corpus — 500 thousand pages — in the night window,
8 workers, everything ready by morning."

```
INPUT
  promise   — 500,000 pages within the night window
  budget    — external limit: the 22:00–08:00 window = 10 hours (CI calendar)
  direction — ceiling (time)

DECOMPOSITION  (fold: product; dimensions: pages × s/page ÷ workers =
               seconds — consistent)
  pages       — 500,000 — measured: wc -l corpus.txt
  time/page   — [0.5 – 2] s — estimate: no faster than pure parsing
                (0.5s, measured on 100 pages), no slower than a fetch
                with retry (2s, last run's log)
  workers     — 8 — a line of the plan (scope, not grounds)
  fold — 500,000 × [0.5–2] / 8 = [8.7 – 34.7] hours

ANCHORS
  0.5–2 s/page vs "HTML parsing — milliseconds, network — hundreds of
  milliseconds to seconds": consistent

VERDICT — factor "time/page" decides: the 10h budget sits inside the
  [8.7–34.7]h range. Measurement (cheapest): run 1000 random pages on
  one worker this afternoon; ≤0.58 s/page → it adds up, more → it
  does not.

  precision note — "ready by morning" against a ×4-wide range — the
    promise is more precise than its own arithmetic
```

## Repeat entry: measured

1000 pages → 1.4 s/page.

```
fold — 500,000 × 1.4 / 8 = 24.3 hours against 10

VERDICT — does not add up: the whole range on the unfavorable side.
  The plan's price of life: ×2.5 workers (up to 20 — if the network
  allows, see altshuller on bans) OR a ×2.5 window, OR convert only
  the delta since the last run (~30k pages → 1.5 hours — adds up with
  ×6 headroom).

  the report's most expensive claim — the measurement was taken by
    day; the night network may be faster
  how it is refuted — the same measurement at 23:00: cheaper than
    discovering it at 6 a.m.
```

The plan died from one measurement and one column of arithmetic —
instead of at 6 a.m. And "delta instead of full run" was born from the
price-of-life line.

## Plan 2: memory — the fold is not about topology

"Run the same 8 workers in a pod with a 4 GB limit."

```
DECOMPOSITION  (fold: SUM — concurrent processes occupy memory
               together; direction — ceiling)
  worker peak — [150 – 400] MB — analog: one worker's RSS in prod
                (metrics, p50–p99)
  workers     — 8
  fold — 8 × [150–400] MB = [1.2 – 3.2] GB against 4 GB

VERDICT — adds up; headroom ×1.25–3.3 — tight: an error in the
  "worker peak" factor eats it (p99 is already 400 MB — one heavy PDF
  hitting all workers at once refutes the range).
```

The fold is chosen by coexistence, not intuition: concurrent workers —
a sum; sequential stages "dump → index" would be a max — the dump has
already returned its memory.

## Why it pays

| | Usual planning | fermi |
|---|---|---|
| "We'll make it overnight" | faith | a [8.7–34.7]h range against 10: one factor decides |
| When you find out | at 6 a.m. | after one daytime measurement |
| "We won't make it" | end of conversation | price of life: ×2.5 workers, ×2.5 window, or the delta |

The numbers met in a column before the deadline met reality — and the
dead plan left three living options.

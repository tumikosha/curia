# The `goldratt` agent by example: "let's speed up the parser"

> **The agent.** `goldratt` reviews by Goldratt's five focusing steps: find
> the system's constraint → exploit it → subordinate everything else →
> elevate → return to step 1. It catches local improvement outside the
> bottleneck — work done well that does not move the system's result
> measure. Input — a system with a goal, the change, and the result measure
> (no measure — refusal). Full definition:
> [`agents/goldratt.md`](../agents/goldratt.md).

A real run against the `http2md` project — a pipeline that turns web pages
into markdown: URL → fetch via Playwright → HTML parsing → markdown.

## The situation

A developer proposes: "The parser is inefficient — I'll rewrite it to be
faster." Sounds reasonable: the code really can be optimized, the work is
well-defined, the result is measurable. A regular code review would assess
the quality of the rewritten parser and approve it.

## Input for the agent

The input contract has three elements:

```
System  — http2md: pipeline URL → HTML → markdown; goal — process pages
Measure — total cycle time for one page
Change  — rewrite the parser (HTML parsing stage) to be more efficient
```

## What the agent answered (abridged)

```
ORDER: violated — a stage improvement proposed before finding the constraint.

STEP 1. CONSTRAINT
  constraint — the fetch stage: Playwright waiting rules
  type       — a policy (not a resource!)
  evidence   — the delays are hardcoded and deterministic:
    - a fresh Chromium per page (~0.3–1 s)
    - networkidle default: +0.5 s minimum, up to 30 s on noisy sites
    - auto-scroll at 100 px / 100 ms: 1 s per 1000 px of page height
    - unconditional wait_for_timeout(1000): +1 s, always
    The parser was actually measured: 11 ms on a typical page, 87 ms on
    a large one. Fetch ≥ 2 s minimum, typically 3–35 s. The parser is
    under 1 % of the cycle.
  refutation test — perf_counter around fetch and md() on 10 real URLs;
    expectation: fetch ≥ 95 % of the cycle.

STEP 2. EXPLOIT — not exhausted; four free reserves on fetch:
  drop the unconditional second, change the networkidle default, speed up
  auto-scroll, reuse the browser (the async path already does).

STEP 4. ELEVATE — not allowed: step 2 is not exhausted.

VERDICT — the work is outside the constraint; contribution to the
  measure: a fraction of a percent. The parser takes 11–87 ms out of a
  2–35 s cycle — even a 10x speedup moves the measure by less than 0.5 %.
  Redirect the work to the fetch waiting rules: a free ~2 s/page minimum,
  up to 30 s on noisy sites.
```

## Where the value is

| | Regular review | goldratt |
|---|---|---|
| What it assesses | quality of the rewritten parser | the work's contribution to the measure |
| Verdict | "the code got better, approved" | "the measure won't move: work is not at the bottleneck" |
| Outcome | a week of work, −50 ms on a 10 s cycle | an hour of fetch fixes, −2…30 s on the same cycle |

The defect "good work in the wrong place" is invisible to a regular
review, because a regular review assesses the change in isolation.
`goldratt` compares it against the system's constraint — and sends the
work back to the one place where it changes the outcome.

The agent also didn't take its own word for it: it **measured** the
parser (11–87 ms), and attached a refutation test to the report's most
expensive claim — if timing on 10 real URLs shows md() > 5 % of the
cycle, the report gets revised.

## Control example: input without a measure

The same question, but no measure of throughput is named:

```
System — http2md: pipeline web page → markdown
Change — speed up the parser
Question — is this the bottleneck? worth doing?
```

The agent's answer is a **refusal**, not a report:

```
REFUSAL — no measure of throughput named; no report is produced.
Define one of: pages/hour end-to-end, or seconds per page, plus a
current measurement. Inventing a measure myself is forbidden.
```

This guards against the LLM reviewer's classic failure — confident
conclusions out of thin air. Without a measure, the word "improvement"
is undefined, and the agent halts the analysis rather than making it up.

## How to invoke

The agent is installed as a symlink at `~/.claude/agents/goldratt.md`.
In a Claude Code session:

> Ask goldratt: [the system and its goal], [the proposed change],
> [the measure of throughput]. Is this the bottleneck?

Read-only: it reads code, measures, proposes tests — changes nothing.

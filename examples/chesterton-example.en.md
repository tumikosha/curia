# The `chesterton` agent by example: "elon proposed demolishing five things"

> **The agent.** `chesterton` checks reasons before demolition, per
> Chesterton's fence: for every proposed deletion it finds the author, the
> original reasons, and whoever has come to lean on the fence; demolition
> with an ununderstood reason is blocked until found out. The antagonist
> pair of `elon`: he proposes deletions, chesterton answers his "bring
> back?" column. Input — proposed deletions: an elon report, a diff, a
> plan. Full definition:
> [`agents/chesterton.md`](../agents/chesterton.md).

A model run on the `http2md` project — the "URL → fetch → HTML parsing →
markdown" pipeline. The input is an `elon` report, step 2: five proposed
deletions. One procedure, five different verdicts.

## The situation

`elon` worked the pipeline over and proposed demolishing: (1) a `sleep(2)`
before fetching every page, (2) the user-agent check-and-override, (3) the
`parse_html_v2` function — a near-duplicate of `parse_html`, (4) `helper.py`,
(5) `handler.py`, the only caller of `helper.py`. Per his return quota he
expects an answer to the "bring back?" column.

A regular review would judge whether the deletion diff is clean. `chesterton`
asks something else: why did each of these fences stand — and do we know it?

## The report (abridged)

```
INPUT
  deletions — elon report, 5 fences; cluster: helper.py + handler.py
              (handler is helper's only caller)
  radius    — the repository
  repeat entry — no

FENCE 1: sleep(2) before fetching
  deliberate — a fence: added by a dedicated commit b3f21a "fix"
  author     — not found: blame leads to a contractor gone since 2024;
               PR without a description; no ticket; not in the docs
  reasons    — "hypothesis": protection against some source's rate limit;
               searched: blame, PRs, issues, docs/, README
  alive      — unknown: the reason is not established
  leaning    — none found (repo-wide grep: no calls, no references)
  reversible — proven: one line, rollback is a one-commit revert
  verdict    — STOP: program — run a 50-URL batch without the sleep in a
               sandbox against the top-5 sources from the logs;
               a 429/ban from any one → "do not demolish" with the reason
               found; clean → the exhaustion rule: reversibility proven →
               "demolish with a sentinel"

FENCE 2: the user-agent check
  deliberate — a fence: test_user_agent_override exists
  author     — found: commit e91c04, author still on the team
  reasons    — established: ticket INC-17 — source N banned the default
               UA of Python libraries (source: commit message → ticket)
  alive      — alive: source N is in the reference corpus pinned in CI
               (fixtures/corpus.txt:12)
  verdict    — DO NOT DEMOLISH: reason INC-17 is alive — source N is
               still being processed

FENCE 3: parse_html_v2 (the near-duplicate)
  deliberate — not a fence: appeared in a meaningless merge commit,
               no test, no neighbor calls it
  leaning    — no living users (grep: the only mention is the file itself)
  verdict    — DEMOLISH: NOT A FENCE — debris from a bad merge

FENCES 4–5: helper.py + handler.py (a cluster, two passes)
  pass 1, each on its own grounds:
    handler — reason established (commit: redirect workaround for
              source M), dead: source M was cut from the corpus in 2025
              (commit 7d0a2e); no hypotheses; no external leaners
    helper  — reasons established and dead (the same ones); its only
              living leaner is handler, from this same input
  pass 2, linkage:
    handler — DEMOLISH; for elon's "bring back?": watch the redirect
              error share in the logs; rollback — a cheap revert
    helper  — DEMOLISH TOGETHER WITH handler: after it or in one commit

SUMMARY
  demolish 3 (1 of them together, 0 with sentinel), do not demolish 1
  (0 inherited or defaults), stop 1 (0 escalations), not-a-fence counted
  under "demolish", refusals 0

  elon's "bring back?" column: sleep(2) — resolved by the stop's program;
  user-agent — bring back (reason alive); v2, helper, handler — no
  elon's quota is not scored until 1 stop is resolved

  the report's most expensive claim — helper's and handler's reasons were
    exhausted by commit 7d0a2e (cutting source M)
  how it is refuted              — grep a month of production logs:
    source M redirects still occur → the reason is alive, both verdicts
    flip to "do not demolish"
```

## Second entry: the stop's program has been executed

The 50-URL batch ran without `sleep(2)` — clean, not a single 429. Repeat
entry: "program executed, the world is silent."

```
FENCE 1: sleep(2) — repeat entry
  verdict — DEMOLISH WITH A SENTINEL (the exhaustion rule: silence after
            an executed program is terminal, reversibility proven).
            Sentinel: the share of 429s/bans in fetch logs; a spike →
            the demolition was a mistake, rollback — revert b3f21a.

SUMMARY (updated)
  stops 0 → elon's quota is scored: returns 1 of 5 — 20%,
  the 10% quota is met
```

The stop did not become an eternal brake: the program was executable, the
world's silence was terminal, and the fence went — with a sentinel, not
with a shrug.

## Why it pays

| | Regular review | chesterton |
|---|---|---|
| What it sees | the deletion diff: clean, tests green | five histories: why each fence stood |
| "Nobody knows why this is here" | an argument for demolition | an argument against — plus a program to find out |
| Verdict | "deletion approved" | 3 demolish, 1 do not (reason alive: INC-17), 1 stop with a program |

The pair with `elon` worked as designed: he dared to propose five
demolitions without knowing the reasons; chesterton dug the reasons up and
put one fence back — exactly the cheap, mandatory return error his quota
counts on.

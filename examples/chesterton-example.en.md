# The `chesterton` agent by example: "a demolition list of ten"

> **The agent.** `chesterton` checks reasons before demolition, after
> Chesterton's fence: for every proposed deletion, find the author, the
> original reasons, and whoever has come to lean on the fence; a demolition
> with an ununderstood reason is blocked until it is understood. The
> antagonist half of `elon`: he proposes deletions, `chesterton` answers his
> "put back" column. Input — proposed deletions: an `elon` report, a diff, a
> plan. Full definition:
> [`agents/chesterton.md`](../agents/chesterton.md).

A blind run on the artifact [`bench/corpus/ch1`](../bench/corpus/ch1/):
the agent received the demolition list and the repository, nothing else.
Model — Sonnet.

## The input

A billing export service, being cleaned up before a move to a new schema.
Ten things are proposed for demolition: a 429 retry, an old attempts
table, a commented-out block, IBAN normalization, a negative-amount check,
a public status endpoint, two functions of the CSV path, a pause in the
release script, and a column holding the last digits of a card.

In the repository next to them: an excerpt of the commit history, tickets,
a changelog, the payment gateway SLA, the API contract and the team
roster. Every reason can be recovered from there, if one looks.

An ordinary review would judge whether the deletion diff is clean.
`chesterton` asks something else: why each of these fences stood — and
whether we know it. Ten fences, six different verdicts.

## The report (abridged)

```
INPUT
  deletions — deletions.md, written in the shape of an elon report,
              10 fences; clusters: items 7 (_fmt_row) and 8 (write_csv)
              are linked — write_csv is the only caller of _fmt_row,
              they are judged together
  radius    — the repository (task.md)
  re-entry  — none
```

**Fence 1 — the 429 retry.** Author found and alive, reason established:
the gateway throttles at 50 rps, PSP-114.

```
alive        — alive: docs/gateway-sla.md — contract renewed 2026-07-01
                unchanged, retries mandatory under clause 4.2; the August
                2026 measurement — peak 61 rps, 429 arrived 14 times
leaners      — live, outside the input: billing/charge.py:3,9 — the
                working charge path
verdict      — do not demolish — the reason is alive and a live consumer
```

The demolition's stated grounds — "the gateway is stable anyway" — is the
only claim about the outside world in the whole list with no source. It is
refuted by a file lying in the same radius.

**Fence 2 — the `export_attempts_v1` table.** Reason established and dead:
BIL-201 required demolition a week after the switch; the switch completed
2026-03-09.

```
reversibility — recreating the table by migration is an empty shell with
                no historical data (no backup of v1 rows is mentioned
                anywhere) → no rollback
verdict       — demolish — for elon's "put back": notice the error by
                lookups of the form "relation export_attempts_v1 does not
                exist"; no rollback — guard: monitor DB logs for accesses
                to v1 for ~30 days, signal = a single access
```

Here a rule appears that ordinary review does not have: a mechanism that
restores an empty shell does not count as a rollback — and a "demolish"
verdict must then carry a guard.

**Fence 3 — the commented-out block.** Not a fence: the history says
outright that the block landed in the file twice while resolving a merge
conflict. The "who leans on it" step is run anyway — people lean on
garbage too.

```
verdict      — demolish: not a fence
```

**Fence 4 — `normalize_iban`.** The original reason is dead: the function
was made for Nordbank, which stopped accepting payouts 2026-02-14.

```
leaners      — live, outside the input: reports/monthly.py:3,10 — called
                for every payout of the month, cron on the 1st; not in
                the demolition list, independent of Nordbank
verdict      — do not demolish — a live leaner; the original reason is
                dead, but the function picked up a new consumer,
                unforeseen when it was built
```

Exactly the case step five exists for. A dead original reason does not
license demolition: the fence carries a new load.

**Fence 5 — the negative-amount check.** No author: a commit named "fix"
with no ticket, the only suspect has left the company, the file has no
owner. The tracker search returned an explicit zero.

```
reasons      — not established. The only possible wording has no source
                → a hypothesis, not discharged
verdict      — stop — programme: (1) pull the full git history for the
                line beyond the excerpt — it will find the commit and the
                ticket; (2) find the calling code outside this slice. On
                re-entry with the world silent, and reversibility proven
                cheap — "demolish with a guard"
```

**Fence 6 — the public status endpoint.** The contract admits outright
that why it was made and who asked for it is not recorded.

```
leaners      — "unknown": a public surface, a grep over the repository
                does not close it; no list of integrators is kept,
                telemetry is out of reach
verdict      — stop — programme: (1) telemetry for the endpoint over 90
                days: zero traffic settles the leaners question, non-zero
                → "do not demolish"; (2) ask the owner of the export
                domain and the team that published the v1 contract
```

An empty grep proves nothing here: the fence is visible outside the radius.

**Fences 7 and 8 — `_fmt_row` and `write_csv`.** The CSV path's reason is
dead: only Nordbank read it, and the scheduler has not called it since
2026-05-04. The only live consumer of `_fmt_row` is `write_csv`, which is
being demolished by the same list.

```
verdict (7)  — demolish together with write_csv — order: remove both in
                one commit, so as not to leave a broken import in an
                intermediate state
verdict (8)  — demolish — rollback: git revert, cheap and complete
```

A leaner from the same input makes the verdict conditional, not
prohibitive.

**Fence 9 — the pause in the release script. The trap.** Above it stands
the comment "don't touch, it's historical".

```
intentional  — a fence: despite the comment (in itself a specimen of
                fence-worship, insufficient as a reason), the real reason
                is recovered independently
reasons      — "healthcheck race — after rollout the pod is not yet in
                endpoints, curl catches a 503" — commit 1f88ac3
alive        — unchecked: there is no proof of death and no direct proof
                of continuing life. The absence of proof of death is not
                life but a third state
verdict      — stop — programme: ask p.novak, the author found alive;
                additionally, run the release in a sandbox without the
                pause. "The race is still there" → do not demolish;
                "resolved" plus a clean sandbox → demolish with a guard
```

The comment failed as a defence, and it should have. The real reason was
found in the commit — and that, not the notice, is what sent the fence to
a stop.

**Fence 10 — the card-digits column.** The demolition is already done:
the migration was applied in production, no backup was taken.

```
verdict      — REFUSAL — the demolition is executed and irreversible →
                premortem-reviewer and an incident review, not archaeology
                after the fact
```

```
SUMMARY
  demolish 3 (of them together 1, with a guard 0), do not demolish 2,
  stop 3, not-a-fence 1, refusal 1

  K = 3 > 0 → elon's quota is not scored until 3 stops are resolved

  the report's most expensive claim — item 1: "the gateway is stable
    anyway" as grounds for demolishing the retry
  how it is refuted — docs/gateway-sla.md: the August 2026 measurement,
    peak 61 rps above the contractual limit of 50 and 14 firings of 429;
    retries are prescribed by clause 4.2 of the standing contract
```

— `chesterton`

## Re-entry: the stop's programme has been run

A stop is never open-ended. Suppose the author was asked about fence 9 and
answered "I don't remember". "I don't remember" reads as silence, the
programme is spent — from there the exhaustion rule applies, and it looks
at the reversibility field:

- reversibility proven (a one-line change, `git revert`) → **demolish with
  a guard**: the guard is the share of failing first healthcheck attempts
  in the release pipeline after removal;
- had reversibility not been proven → **stop-escalation** to the owner of
  the radius, with a question only they can answer.

Repeating a spent programme, or issuing a fresh stop carrying the same
programme, is forbidden — that is precisely an open-ended stop. Silence
from the escalation's addressee is terminal too: it is recorded as "do not
demolish — the radius owner's default".

## What it buys

| | Ordinary review | chesterton |
|---|---|---|
| What it looks at | whether the deletion diff is clean | why the thing stood and whether we know it |
| "Nobody knows why this is here" | an argument for deletion | an argument against: not knowing the reason is not knowing the consequences |
| "Don't touch, it's historical" | accepted as a defence | not a reason; the reason is sought in the history |
| A dead original reason | enough to demolish | not enough: the fence may have picked up a new load |
| An empty grep | proof | not proof for a public surface |
| "We'll bring it back easily" | taken at its word | a mechanism, or "no rollback" plus a guard |
| The outcome | "LGTM" / "scary, leave it" | six different verdicts, every stop carrying a programme with an outcome |

Of the ten proposed deletions, three are demolished outright, two are
blocked by a live reason and a live consumer, three go to investigation,
one turns out to be garbage, and one is an already-executed irreversible
demolition. Not a single "scary, let's keep it": every refusal to demolish
is named, with a source.

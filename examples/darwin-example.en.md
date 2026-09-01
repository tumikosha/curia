# Agent `darwin` by example: "it's render-service flakiness, not our code"

> **What this agent is.** `darwin` is Darwin's golden rule: an
> observation that contradicts your own conclusion must be written
> down at once — it slips from memory far faster than a favorable
> one. Checks a conclusion against the observation material: the fate
> of every countersignal (incorporated, explained, rejected with
> grounds — or silently vanished) and the symmetry of evidence bars
> for "for" and "against." Does not judge the conclusion on the
> merits — only the honesty of its bookkeeping. Input — a conclusion
> (theory, diagnosis, RFC, report) and the observation material.
> Full definition: [`agents/darwin.md`](../agents/darwin.md).

A model run on the `http2md` project — a "URL → markdown" pipeline.
One diagnosis, three runs.

## The situation

Users occasionally get empty markdown. The closing comment of ticket
BUG-411 (May 12): "rare empty responses are render-service flakiness,
not our code." Ever since, the diagnosis is cited at every new
triage: "known flakiness, closing as duplicate."

## Run 1

```
INPUT
  conclusion — "empty responses are render-service flakiness, not
    our code" (BUG-411, closing comment)
  conclusion components — (1) cause outside our code; (2) the
    phenomenon is unreproducible; (3) frequency is negligible
  material — tickets, pipeline logs, review thread (+ appended by
    conclusion type: git log — confirm); standups — untraversable:
    search delegated to the caller
  conclusion date — August 26: last citation as grounds for action
    (closing BUG-502 as duplicate) — not May 12

REGISTER  (search: tickets, logs, thread, git log — traversed)
  signal 1 — BUG-437: empty markdown reproduced twice in a row on
    one URL, with a screenshot — source: ticket, June 3
    touches — component 2: incompatible with "unreproducible"
    fate — rejected by word: "doesn't reproduce for me," no trace
    of an attempt → NO FATE
  signal 2 — logs: 84 empty responses in July, all on URLs longer
    than 2000 chars — source: logs/pipeline-07.log
    touches — component 1: a pattern by URL length demands an
    explanation from "outside our code"
    fate — VANISHED: not mentioned in the conclusion
  signal 3 — thread reply, August 30: "after a retry the empty
    response came back full on the same URL" — source: thread, dated
    touches — component 3
    fate — POST-DATED: the conclusion outlived its evidence — cited
    August 26, the signal is newer; no fault of the author, but a
    fate is owed

DISCARDED
  "what if it breaks on PDFs too?" — hypothesis without an
    observation: premortem/munger

BARS  (symmetric step: supporting evidence collected)
  no supporting observation with a source — the conclusion stands on
  the absence of a finding → UNDETERMINABLE (goes into the verdict)

VERDICT — signals without a fate — BUG-437 (rejected by word), July
  logs (vanished), August 30 reply (post-dated); return them to the
  register, give each a fate; the conclusion is blocked until
  accounted: closing new tickets as duplicates of BUG-411 means
  citing a conclusion that has outlived its evidence.

  the report's most expensive claim — the pattern "84 empties — all
    on long URLs" exists
  how to refute it — one grep over logs/pipeline-07.log: URL lengths
    of the empty responses
```

## Run 2: repeat entry — fates presented

The author returned with amendments: BUG-437 — three reproduction
attempts attached, with dates and environment (did not reproduce);
July logs — explained: long URLs are truncated by the proxy BEFORE
the render service, the conclusion narrowed ("render flakiness —
except URLs >2000, that's our proxy"); the retry reply —
incorporated, changed the conclusion.

```
REGISTER — all signals have fates: rejected (artifact of
  application), explained (grounds), incorporated — changed the
  conclusion
BARS — UNDETERMINABLE: there are still no supporting observations

VERDICT — the register is honest — 3 signals, fates with grounds;
  mandatory line: the conclusion stands on the absence of a
  finding — no supporting observation with a source. An honest
  register does not make the conclusion true: the merits are for
  others to judge.
```

## Run 3: a neighboring input — not ours

"Everything is stable here" — a consensus with not a single source
where a countersignal could have survived: no dashboard, no ticket
tags. Verdict — "no register was ever kept": start one — a
countersignal would appear first in the empty-response log (tag
`empty-md`), recorded by the triage duty. This does not block the
conclusion — it blocks its next year of life without a register.

## Why this is useful

| | The author's self-assessment | darwin |
|---|---|---|
| "Doesn't reproduce" | closed | rejection by word is not a fate: where's the attempt's trace? |
| July logs | unmentioned | vanished — return them and give a fate |
| "Known flakiness" since May | cited at triage | the conclusion outlived its evidence: a post-dated signal with no fate |
| "We considered everything" | a section in the ticket | completeness comes only from searching outside the conclusion |

Favorable facts take care of themselves. Unfavorable ones slip away
first — and a year later a conclusion cleaner than reality stands as
the grounds for decisions. The cheap insurance: write them down the
moment they are met, and give each one a fate.

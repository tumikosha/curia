# Agent `ohno` by example: "worker crashed — we raised the memory limit"

> **What this agent is.** `ohno` is Taiichi Ohno's five whys plus
> genchi genbutsu: does the causal chain reach a root whose removal
> kills the class of recurrences, and does every link stand on what
> was seen at the site rather than on hearsay. Five is a heuristic:
> stopping is judged by the root test (a process — not a person, a
> class — not an instance, an ownership boundary — with an
> addressee). Catches symptom fixes, chains cut off at "the engineer
> made a mistake," and links built on assumption. Input — a symptom
> and the analysis of its causes (postmortem, RCA, a fix with
> rationale). Full definition: [`agents/ohno.md`](../agents/ohno.md).

A model run on the `http2md` project — a "URL → markdown" pipeline.
One incident, three runs.

## The situation

At night the conversion worker crashed: OOM. In the morning — user
complaints. The postmortem: "cause — large pages; fix — raised the
memory limit from 2 to 4 GB." Closed.

## Run 1

```
INPUT
  symptom — worker OOM, downtime until morning (INC-77)
  analysis — postmortem: OOM ← large pages; fix — 4 GB limit
  how caught — users, in the morning → detection branch MANDATORY

CHAIN
  branch "why it happened"
    link 1 — OOM caused by large pages — evidence: dmesg quote with
             path, medium verified (logs/kern-0829.log)
    root — "large pages" — root test: NOT PASSED — that's weather,
           not a process: large pages will always exist; an
           arbitrary stop
  branch "why we didn't catch it" — ABSENT: per-branch verdict
    "no analysis" for it

COUNTERMEASURE
  4 GB limit — PALLIATIVE without a note: a 5 GB page will bring
  the incident back under a different number

VERDICT — worst of the branches: no analysis (detection branch) +
  chain cut off (main). First whys for detection: why is worker
  memory not trend-alerted? Next whys for the main branch: why does
  one page eat gigabytes — what does the parser hold in memory?
  Candidates with evidence: parser/dom.py, the alerts config.

  the report's most expensive claim — "large pages" is weather,
    not a root
  how to refute it — show the process that decides how much memory
    an input may consume; there is no such line in the repo
```

## Run 2: repeat entry — the chain extended

```
CHAIN
  branch "why it happened"
    link 1 — OOM while converting a ~200 MB HTML page — evidence:
             dmesg quote, verified
    link 2 — at crash time there was a spike of large pages from one
             domain — UNPROVABLE: medium lost — metrics retention is
             7 days (prometheus.yml: retention 7d), the incident is
             a month old
    link 3 — the parser builds the full DOM in memory, no streaming
             mode — evidence: parser/dom.py:41-58, read
    root — CI has no memory-consumption gate for the class of large
           inputs — root test: class named (PDFs, long threads,
           auto-generated pages); history search: INC-52 (OOM on a
           PDF, six months ago) — same root
  branch "why we didn't catch it"
    link 1 — no trend alert on worker memory — evidence: alerts
             config, read
    root — the alert-creation process covers only HTTP errors, not
           resources — class: any resource failure

BACKWARD PASS — holds; link 2 is not load-bearing: the root stands
  on link 3 (code), not on the spike

COUNTERMEASURE
  memory gate in CI on a large-input corpus — claimed — confirm
    (.ci/mem-gate.yml doesn't exist yet)
  4 GB limit — palliative WITH a note: until the gate, replacement
    trigger named
  memory trend alert — claimed — confirm

VERDICT — root reached (both branches) — conditional: countermeasures
  are "claimed," present the configs. Class: INC-52 from history —
  same root, two pieces of class evidence. Link 2 unprovable — does
  not affect the verdict: the root stands on code, not on the spike.
```

## Run 3: a neighboring postmortem — "the junior forgot"

A neighboring team: "incident cause — the junior forgot to update
the config after the migration." A chain cut off at a person: a name
in the root is the mark of an unfinished chain, not a finding. Next
whys: what process allowed a forgotten config to reach production?
Candidates: the config isn't validated in CI (check: .ci/), the
migration carries no checklist, the deploy doesn't cross-check
config and schema versions. "Be more careful" is not a
countermeasure.

## Why this is useful

| | The postmortem | ohno |
|---|---|---|
| "Cause — large pages" | closed | that's weather, not a process: no class named |
| 4 GB limit | a fix | palliative without a note: it will return under another number |
| Caught by users in the morning | unmentioned | the mandatory "why not caught" branch is absent |
| "The junior forgot" | culprit found | a cut-off chain: what process allowed it? |

Five whys is not a ritual of depth but the road from an instance to
a process. The cause lives at the site — in the code, the log, the
config — not in the report about the site; and the countermeasure
belongs where the class of recurrences dies, not just this one
incident.

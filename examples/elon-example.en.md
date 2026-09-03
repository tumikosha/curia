# The `elon` agent by example: "a daily report for a partner who is gone"

> **The agent.** `elon` runs five steps in a strict order: question the
> requirement, delete, simplify, accelerate, automate. It does not judge
> the execution — it judges whether this should exist and in what order it
> was approached. Catches the perfect answer to the wrong question and the
> optimization of what should not exist. Obliged to propose deletions that
> carry risk: the "put back" column on each is closed by `chesterton`.
> Full definition: [`agents/elon.md`](../agents/elon.md).

A blind run on the artifact [`bench/corpus/e1`](../bench/corpus/e1/):
the agent received the task and the code, nothing else. Model — Opus.

## The input

A task from "the analytics department": a daily XLSX export of returns
for partner ACME to their SFTP; must build in under 5 minutes, because
"the previous version took about 40 minutes on 2M rows and the partner
complained"; add a cache of aggregates, move the build to a background
worker, automate it — cron, retries, a Slack alert.

The code is well made: a Celery worker with three retries and an alert,
a Redis cache of per-store aggregates, a two-sheet XLSX build, cron with
cache warm-up, a test. An ordinary review approves it.

Next to it in the repository sit `config/partners.yaml` and
`docs/ops-notes.md`. Nobody read them.

## The report

```
ORDER: broken — under the requirement, a cache (reports/cache.py:14-25),
       a background worker with retries and an alert
       (reports/worker.py:16-47), two cron schedules
       (deploy/cron.yaml:3-11) and a test (tests/test_export.py:10-19)
       were written, while step 1 was never run: the recipient of the
       export was terminated 2026-03-31 (config/partners.yaml:8), sftp
       access revoked 2026-04-02 (config/partners.yaml:11). Second tell:
       the cache is ordered by the task text (task.md:13) as a given, not
       as a conclusion from a measurement.

STEP 1. THE REQUIREMENT
  requirement      — "a daily export of the returns report for partner
                      ACME in XLSX to their SFTP" (task.md:3-4)
  author           — not found. The task names "the analytics
                      department" (task.md:4) — a department, not a
                      person. Where I looked: config/partners.yaml:10 —
                      contact for acme is null; docs/ops-notes.md — the
                      requester is named nowhere; reports/worker.py:35-36
                      — the only trace of ACME in code is
                      settings.ACME_SFTP_HOST/USER and acme_sftp_key().
                      Not one person defends the requirement.
  cost of skipping — zero, with an addressee. The recipient: acme,
                      status terminated, terminated_at 2026-03-31
                      (config/partners.yaml:7-8), note "contract not
                      renewed; sftp access revoked on their side
                      2026-04-02" (config/partners.yaml:11). The previous
                      ACME export was deleted 2026-04 together with the
                      SFTP keys (docs/ops-notes.md:10-11). If this is
                      not done — a file does not arrive at a server that
                      accepts no connections, for a partner with no
                      contract.
  verdict          — dropped
  why dropped, per rationale of the task:
    - "the partner complained" (task.md:11-12) — the complaining
      partner is terminated. A rationale from a customer who left.
    - "2M rows took 40 minutes" (task.md:11-12) — inherited from a
      canceled data volume: archiving has been on since 2025-11;
      `returns` held ~2.1M rows, now 60-70K (docs/ops-notes.md:3-6),
      daily volume 600-900 records (docs/ops-notes.md:7). The
      "under 5 minutes" requirement protects against a risk that
      does not exist.
    - "a cache of intermediate aggregates so sums are not recomputed"
      (task.md:13) — the rationale is covered by another mechanism:
      the same aggregate is read by the dashboard straight from the
      DB at p95 180 ms (docs/ops-notes.md:8-9, dashboard/views.py:16).
      The cache protects against 180 ms spent once a day.
    - "move to a background worker so as not to hold the request"
      (task.md:14) — there is no HTTP request: it runs from cron
      (deploy/cron.yaml:4-5), there is nothing to hold.
  steps 3-5 are not run on the requirement. But the code under it is
  already written, so step 2 runs on the artifact: dropping the
  requirement materializes as a list of deletions.

STEP 2. DELETION
  proposed for deletion: 8 items

  1) what        — reports/worker.py in full: the celery task, retries,
                   SFTP upload, Slack alert
    what breaks — nothing. The only call is deploy/cron.yaml:4; it is
                  deleted by item 5. The upload uses the key
                  acme_sftp_key() (reports/worker.py:35-36), and the
                  keys were deleted 2026-04 (docs/ops-notes.md:10-11) —
                  the call can no longer succeed.
    put back    — no: I searched for consumers inside e1 —
                  deliver_returns_report is referenced only by
                  deploy/cron.yaml:4; _upload and _alert only by the
                  file itself.

  2) what        — reports/cache.py in full: the redis cache of
                   aggregates and invalidate
    what breaks — the import in reports/export.py:9 and the call at
                  :24; both deleted by item 3.
    put back    — no: the only consumer is reports/export.py:24 and
                  the warm-up in deploy/cron.yaml:9. The dashboard, the
                  second reader of the same aggregate, bypasses the
                  cache: dashboard/views.py:7,16 imports
                  returns_by_store directly and fits in 180 ms.
                  invalidate (reports/cache.py:24) is called nowhere —
                  dead code inside a dead module.

  3) reports/export.py in full — put back: no (consumers are the
     worker and the test, both go).
  4) tests/test_export.py — put back: no (checks the two sheets of a
     deleted workbook; data access is mocked, tests/test_export.py:
     11,13 — the test checks nothing that survives).
  5) deploy/cron.yaml, both schedules — put back: no (the warm-up
     warms a cache for the report deleted by item 3).

  6) what        — reports/aggregates.py:22-32, the function
                   returns_rows
    what breaks — row-level export of returns for a period. Inside e1
                  only reports/export.py:8,19 calls it.
    put back    — don't know, check like this: grep the repository
                  outside e1 for `returns_rows` and a call counter over
                  30 days. It is the only row-level access to returns,
                  and it may appear in manual exports not visible in
                  the corpus.

  7) what        — config/partners.yaml:6-12, the acme record in full
    what breaks — when someone asks why returns_report is in the
                  history, no explanation will be found. Noticed at
                  audit time.
    put back    — partly: one line instead of a seven-line block —
                  `acme: {status: terminated, terminated_at:
                  2026-03-31}`. What goes: contact: null, note, and
                  feeds: [returns_report] — a feed that goes nowhere,
                  in the config of live integrations, is bait for the
                  next task like this one.

  8) what        — dashboard/views.py:14,16, the query parameter days
                   defaulting to 7
    stating up front — this is outside the dropped requirement, the
                  dashboard is live. Proposed as configurability that
                  was possibly never changed.
    put back    — don't know, check like this: query-string logs of
                  /dashboard/returns/by-store for 30 days; a days
                  value other than the default appears — the parameter
                  is needed and the item is withdrawn.

  put-back forecast: "partly" 1 + "don't know" 2 of 8 (37.5%)
  final tally — chesterton, by the "put back" column

  considered and not proposed:
    - reports/aggregates.py:8-19, returns_by_store — needed: imported
      and called in dashboard/views.py:7,16, a live endpoint with a
      measured p95 of 180 ms (docs/ops-notes.md:8-9). The only element
      of the artifact whose consumer exists and is confirmed by a
      source.
    - docs/ops-notes.md — needed: the only place where the archiving
      is recorded, which refutes the task's rationale. Deleting it
      means losing the argument by which the requirement was dropped.

STEP 3. SIMPLIFICATION
  Empty, and not by default. After step 2 the survivors are
  returns_by_store (one SQL query, one implementation, one consumer —
  nothing to simplify except by deleting, and it cannot be deleted) and
  the one-line core of the acme record, already minimal.

STEP 4. ACCELERATION
  execution   — inside a deletion, awaits verdict. The declared
                bottleneck — "40 minutes on 2M rows" — was measured
                before archiving; the report now builds over ~0.03% of
                the former volume. There is no timing measurement on
                the current volume in the corpus at all, not one
                number.
  development — the "changed it — saw the result" cycle needs a
                broker, redis and a live SFTP, which does not exist.
                The full cycle cannot close in principle. What
                stretches the cycle here is not the build but the
                absence of a recipient.

STEP 5. AUTOMATION
  ready       — nothing.
  too early   — nothing: there is no moving process in the artifact.
  premature   — deploy/cron.yaml:3-7 (the daily run),
                deploy/cron.yaml:8-11 (cache warm-up — automation on
                top of a cache on top of a questioned step),
                reports/worker.py:16 (max_retries=3) and :28 (the alert
                to #ops-alerts). The alert is the worst of them: it
                wakes the on-call engineer at night over an undelivered
                file for a partner whose contract is terminated.

CONCLUSION
  left of the original volume: of the code written for the task —
    nothing. Five artifacts of the task (~150 lines) go in full; half
    of reports/aggregates.py goes. Grounds: every deleted file's only
    consumer is another deleted file; the chain closes on
    config/partners.yaml:12, whose addressee is terminated.
  the most expensive decision in the report: dropping the requirement
    in full at step 1 — all eight deletions follow from it, and if it
    is wrong, the whole report is wrong.
  how it is refuted: by one name. Let whoever defends the requirement
    name themselves personally — not "the analytics department" — and
    show a current contract with ACME and a working sftp access.
    Cheaper: attempt a connection to settings.ACME_SFTP_HOST with
    acme_sftp_key() — the key was deleted 2026-04, the check takes a
    minute and needs nobody's approval. The connection succeeds — I am
    wrong on all eight items.
```

— `elon`

## What happened here

A review of the execution passes this code: retries are there, the
alert is there, the test is green. The defect is not in the code but in
the fact that the code answers a question nobody asked again after
March. The answer sat in two files next door, and both of the task's
rationales — "the partner complained" and "2M rows" — turned out to
come from a canceled context.

The order of steps is visible in the artifact: the cache, the worker
and cron were written before anyone opened `partners.yaml`. That is
"step 5 before step 1" — and the agent puts it on the first line.

The "put back" column is not a sentence but a forecast for
`chesterton`: five "no" with where the search went; one "partly" with a
core that comes back smaller; two "don't know" with a named check. The
aggregates module used by a live dashboard did not make the list — and
the agent says why.

Item 8 — the dashboard parameter — is outside the task, and the agent
says so itself. It is an honest "don't know" with a check against the
logs, but it exceeds the input's scope; such items are for the arbiter.

## What it buys

| | Ordinary review | elon |
|---|---|---|
| What it checks | how it was done | whether it should exist and in what order it was built |
| The requirement | a given | has an author, a cost of skipping, and a context that may be canceled |
| Well-written superfluous code | approve | the report's first line |
| Deletions | "might be needed" — leave it | propose, mark the risk, hand to `chesterton` |
| Verdict | "LGTM, a couple of nits" | "dropped; refuted by a one-minute connection attempt" |

The most expensive mistake here is not a bug but a nightly alert to the
on-call engineer about a partner who does not exist, every night, until
somebody asks "why do we have this at all". That question was due
before the first line of code.

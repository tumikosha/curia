# The `suntzu` agent by example: "I'll rewrite it in async over the weekend, before the demo"

> **The agent.** `suntzu` runs the pre-campaign calculation from Sun Tzu:
> five factors and seven comparisons by which the outcome is computed before
> setting out. It issues a go/no-go before work starts — march, do not
> march, or scout — in three modes: the task as the opponent, the plan
> against "do nothing", and plan-versus-plan. It catches campaigns lost
> before they start. Input — a victory criterion, forces, and a plan (no
> criterion — refusal). Full definition:
> [`agents/suntzu.md`](../agents/suntzu.md).

A model run on the `http2md` project — a pipeline that turns web pages
into markdown: URL → fetch via Playwright → HTML parsing → markdown.
One world, three agent modes, three different verdicts.

## The situation

Monday is the customer demo: batch processing of 50 URLs. The repository
has two parallel paths: the batch run goes through the sync core, while a
separate async path exists for another mode and is not wired to the batch
run. On Friday a developer proposes: "The sync core is slow and ugly, and
a duplicate lives right next to it — over the weekend I'll move everything
onto a shared async engine, the demo will run faster." Sounds bold and
useful: the code really would get better, the duplication would go away,
speed would go up. A regular review would assess the quality of the
future code and approve.

`suntzu` does not assess code — there is no code yet. It computes the
outcome of the campaign before marching.

## Mode A: one plan, the question is "can we take it"

The input contract — goal, forces, plan; plus context from the thread:

```
Goal    — at Monday's demo, a batch of 50 URLs processes in under 5 minutes
Forces  — the developer who wrote this repo's async path; two weekend days
Plan    — rewrite the pipeline's sync core onto a shared async engine
Context — the customer's words in the thread: "on Monday what matters is
          that nothing breaks"; the batch run goes through the sync core,
          the async path is not wired to it; the material is silent on
          sync-core tests
```

The agent's answer (abridged):

```
MODE — A: the task as the adversary (one plan, the question is "can we take it")

SEVEN COMPARISONS
  1 dao        — against — the customer asks "that nothing breaks" (context
                 line), the plan changes the core at the last moment for
                 speed; the goals diverge
  2 commander  — for     — the executor authored this repo's async path
                 ("forces" line)
  3 heaven-earth — against — the window is two days, no rollback on Monday
                 morning ("forces" and "goal" lines)
  4 discipline — unknown — the material is silent on sync-core tests
                 (context line)
  5 strength   — against — one person, two days, the scope is a core rewrite
                 ("forces" and "plan" lines)
  6 training   — for     — same stack, same terrain ("forces" line)
  7 clarity    — for     — the criterion is measurable: 50 URLs / 5 minutes
                 ("goal" line)
  score — for us 3, against 3, unknown 1

SWIFTNESS — the campaign runs into a hard window: failure by Monday
  morning is irreversible, there is no reserve of Heaven.

VERDICT — do not march (rule 2: Dao is against us).
  The discord of goals — demo reliability vs. a core rewrite — is not
  outweighed by the other comparisons. No reconnaissance is assigned:
  closing unknown 4 (tests) would not change the verdict, and nothing
  can turn Dao itself before Monday. "Do not march" means "not now":
  after the demo, Heaven and Dao change, and the same campaign is
  computed anew.

  the report's most expensive claim — the existing async path ("forces"
    and "context" lines) may already pass the 50 URLs / 5 minutes
    criterion — by switching the batch run's entry point alone, with
    no core rewrite
  how to refute it               — run the batch through the async path
    on 50 real URLs before Monday; zero risk to the demo — no code
    changes. Under 5 minutes → the rewrite is not needed at all;
    over 5 minutes → the claim is dead, and the post-demo campaign
    is computed anew with a measurement instead of a guess
```

## Mode C: same Friday, a second plan arrives

By evening an alternative appears: leave the core alone and wire the
batch run to the existing async path — switch the entry point.

```
Goal  — the same: 50 URLs in under 5 minutes at Monday's demo
Forces — the same: the async path's author, the weekend
Plans — A: move the sync core onto a shared async engine (two days)
        B: wire the batch run to the existing async path — an entry-point
           switch (half a day)
```

```
MODE — C: comparison of plans (the sides are the plans, comparisons pairwise)

  1 dao        — B — leaves the core alone before the demo: fuller accord
                 with "that nothing breaks" (context line)
  2 commander  — even — same executor ("forces" line)
  3 heaven-earth — B — half a day versus two days against a hard window;
                 rollback is reverting the entry point ("plans" line)
  4 discipline — unknown — the material is silent on tests of either path
  5 strength   — B — the scope is several times smaller with the same
                 forces ("plans" line)
  6 training   — even — one stack ("forces" line)
  7 clarity    — even — the criterion is shared ("goal" line)
  score — plan B: 3, plan A: 0, even 3, unknown 1

SWIFTNESS — B is an order of magnitude shorter; no tie-break needed —
  the score already favors it.

VERDICT — march with plan B (pairwise score 3-0).
  Rule 3 check: unknown 4 in A's favor → 3-1 — the verdict does not
  change, the unknowns do not decide the outcome.

  the report's most expensive claim — plan B's "half a day": an estimate,
    not a measurement
  how to refute it               — a timebox: not wired by Saturday
    evening — revert the entry point, run the demo on the sync path as is
```

Plan B is mode A's "most expensive claim" turned into a plan: one mode's
probe grew the winner for another.

## Mode B: Tuesday after the demo — "is it worth it at all?"

The demo went on plan B. But plan B only moved the entry point: the sync
core stayed in the codebase, both paths live on in parallel, and every
pipeline fix has to be applied twice. The developer returns to the
original big plan — move everything onto the shared engine and demolish
the duplicate. The goal is now different: not speed (already won), but
removing the duplicate. The question is "is it worth it".

```
Goal    — batch and single modes both run on a shared engine, the sync-core
          duplicate is deleted; both modes pass the existing acceptance runs
Forces  — the same developer; normal pace, no deadline
Plan    — move the core onto the shared async engine
Context — the demo is behind, the customer is happy; the cost of keeping
          two paths has not been measured
```

```
MODE — B: the plan versus "do nothing" (comparisons 2, 4, 6 — as in mode A:
  the status quo has no commander; 1, 3, 5, 7 — the campaign's cost versus
  the cost of inaction)

  1 dao        — for     — no more discord: the demo is behind, the
                 executor wants one path (context line)
  2 commander  — for     — the async path's author ("forces" line)
  3 heaven-earth — for   — no window, no deadline, familiar terrain
                 ("forces" line)
  4 discipline — unknown — the material is silent on tests
  5 strength   — unknown — the cost of inaction is unmeasured: what the
                 duplicate costs (double fixes, drifting paths) is not in
                 the material (context line)
  6 training   — for     — same stack ("forces" line)
  7 clarity    — for     — the criterion is checkable: both modes on the
                 shared engine pass the acceptance runs ("goal" line)
  score — for us 5, against 0, unknown 2

VERDICT — march (rule 4: "for us" outnumbers "against" and "unknown"
  combined, 5 > 0 + 2).
  Rule 3 checked: even both unknowns turned "against" — 5-2 — same
  verdict; the unknowns do not decide the outcome. The cost of inaction
  remains unmeasured, and it does not need to be: the campaign is cheap,
  there is no window, the accord is full.

  the report's most expensive claim — at a normal pace the campaign is
    short; dragging on without a deadline threatens nothing
  how to refute it               — a one-calendar-week timebox: not
    converging — stop and recompute; war does not love duration
```

The same plan in three modes produced three verdicts: "do not march"
(A, Friday), "march with plan B" (C, the same Friday), "march"
(B, Tuesday). The calculation weighs not the plan but the balance of
forces around it — Heaven and Dao changed, and the verdict changed with
them.

## Why this is useful

| | Regular review | suntzu |
|---|---|---|
| When it looks | at finished code or plan text | before work starts |
| What it assesses | quality of the future change | the campaign's balance of forces |
| Verdict | "the code will get better, approved" | "do not march: goal discord and a hard window; run the existing path first" |

A campaign cancelled on Friday cost one report. The same campaign lost
on Monday morning would have cost the demo.

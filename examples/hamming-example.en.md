# The `hamming` agent by example: "two weeks on a beautiful CLI theme"

> **The agent.** `hamming` asks the three questions from "You and Your
> Research": what are the important problems of the field, which of them is
> this work on, and if none — why. The importance test: an attack, compound
> interest, consequences for the field. It catches well-executed unimportant
> work and portfolios of safe trifles. Input — the field and the work (one
> item or a portfolio over a period), ideally with a list of important
> problems. Full definition: [`agents/hamming.md`](../agents/hamming.md).

A model run on the `http2md` project — a pipeline that turns web pages into
markdown: URL → fetch → HTML parsing → markdown. One world, four runs, four
different verdicts.

## The situation

The repository contains a `ROADMAP.md` authored by the owner, first line:
"P0: pages with JS rendering produce empty markdown — half of the real web
is unreachable for the converter." Meanwhile a developer spent two weeks on
a CLI theming system: colored progress bar, logo, palette config. Superbly
done — tests, documentation, clean code. A regular review would praise it
and approve.

`hamming` does not look at quality — it asks the lunch-table question: what
are the important problems in your field, and which of them was this work on?

## Run 1: finished work, no list in the input

```
Field         — http2md: the "URL → markdown" pipeline; the result is a
                converter you can feed the real web to
Work          — done: CLI theming system; two weeks
Important problems — not provided
Task choice   — the developer picks their own tasks
Work size     — two weeks (from the input)
```

The agent's answer (abridged):

```
INPUT
  important problems — from an owner-authored document: ROADMAP.md
                       (git author — the repository owner) — confirm freshness

QUESTION 1. IMPORTANT PROBLEMS OF THE FIELD
  JS rendering — attack: exists — angle of approach: a headless browser is
                 already among the dependencies; first step: capture the DOM
                 after page load
               — compound interest: opens the SPA half of the web; everything
                 else will lean on it — batch mode, caching, acceptance
               — consequences: the converter starts working on the modern
                 web, not just static pages
               — source: ROADMAP.md:1 — confirm freshness

QUESTION 2. WHICH OF THEM IS THIS WORK ON
  none — CLI themes neither attack JS rendering nor prepare an attack:
  the output is prettier, the share of processed pages is unchanged
  (the diff touches neither fetching nor parsing)

QUESTION 3. IF NONE — WHY
  reason — reconstructed: "wanted to finish and polish something visible"
  class  — rationalization: "it is safer" (the input confirms: picks
           their own tasks)

VERDICT — well-executed unimportant work.
  Sitting idle: JS rendering — with an attack via the headless browser.
  Diverted effort: two weeks (input line).
  Reason for straying — the "safer" rationalization.
  Pre-verdict checks: no shared result measure named in the input — no
  redirect to goldratt; an alternative is named — elon's zone untouched.

  the report's most expensive claim — CLI themes feed JS rendering in no way
  how it is refuted                 — the caller names which attack the
    themes prepare and how; nothing to name — the verdict stands
```

Note: the verdict never touched the quality of the work. Praising execution
hides the defect — which is why there is none in the report.

## Run 2: before starting, "feeds"

A day later the same developer brings a plan: "I will build a corpus of 200
real pages with reference markdown fixtures and a CI run."

```
QUESTION 2 — feeds JS rendering: a corpus with references is the acceptance
  harness of the future attack; without it, victory over JS pages is
  unmeasurable (source: plan line; ROADMAP.md:1)

VERDICT — the work feeds the important problem JS rendering — proceed.
  Contribution: makes the attack verifiable — a reference corpus turns
  "it got better" into a count of passing pages.
```

The corpus is not the attack itself and looks humbler than CLI themes.
Importance is measured not by flashiness but by what will lean on it next.

## Run 3: a typo fix

Fixing a typo in the README, the diff is one line.

```
QUESTION 3 — class: not applicable (verdict "trifle")

VERDICT — a trifle — not a finding (size: 1-line diff).
  A portfolio of trifles is judged on a portfolio input.
```

A single trifle is amnestied: it took no effort away from what matters.
Branding a typo fix is a false positive, and the verdict rule forbids it.

## Run 4: a quarter's portfolio

The owner brings a set: 12 works over the quarter — CLI themes, three
renaming refactors, README badges, typo fixes, linter config.

```
Rules 1–7 applied to every work in the set; the list is the owner's ROADMAP.md:
  CLI themes      → rule 7 (unimportant; JS rendering sits idle)
  the other 11    → rule 6 (trifles) or rule 7

Portfolio outcome — a portfolio with no important work: not one all quarter.
  No work in the set earned "directly" or "feeds", while a problem with an
  attack stood in ROADMAP.md:1 the entire quarter.

  the report's most expensive claim — JS rendering was attackable all quarter
  how it is refuted                 — the owner names the blocker that made
    the attack unavailable (no environment, waiting on a decision); once
    named, the portfolio's class shifts from rationalization to "did not
    choose"
```

On a single work this defect is invisible: each trifle is legitimate on its
own. The portfolio is the only input on which it can be pronounced.

## Why it pays

| | Regular review | hamming |
|---|---|---|
| What it sees | the CLI theme code: clean, tested | ROADMAP.md:1 idle for two weeks |
| Verdict | "excellent work, approved" | "well-executed unimportant work: JS rendering with a ready attack sits idle" |
| Blind spot | whether it was worth doing | execution quality — deliberately |

Good execution is not an answer to "why not the important problem."
Objections to the verdict — "the themes feed acceptance", "JS rendering was
blocked" — are exactly the substantive conversation the agent exists for:
it starts from the verdict, not instead of it.

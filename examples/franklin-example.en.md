# The `franklin` agent by example: "telemetry on by default?"

> **The agent.** `franklin` runs the moral algebra from the 1772 letter to
> Priestley: two columns of reasons and striking out the balanced instead of
> counting; the remainder is the decision. Two kinds of weight judgments —
> equivalence and dominance — both auditable and confirmed by the decider;
> the agent invents no weights. It catches counting instead of weighing — a
> crowd of light reasons against one heavy one. Input — a binary decision,
> reasons, material. Full definition:
> [`agents/franklin.md`](../agents/franklin.md).

A model run on the `http2md` project — the "URL → markdown" pipeline. One
decision, two passes, and one redirect.

## The situation

The team is arguing: should the CLI send telemetry by default — the
processed URLs, to prioritize the reference corpus? They voted: four
reasons "for", two "against" — "majority says enable." `franklin` exists
precisely against that way of deciding.

## Pass 1: columns, judgments, a question

```
INPUT
  decision — telemetry on by default: yes / no
  decider  — the project owner
  reasons  — from the caller: 4 for, 2 against; gathered by the agent: 1
  repeat entry — no

COLUMNS
  FOR
    F1 corpus prioritization from real URLs — input line
    F2 failing sources surface faster — input line
    F3 a metric for the project write-up — input line
    F4 "everyone has telemetry" — input line
  AGAINST
    A1 users send us their URLs — privacy — input line
    A2 GDPR handling of addresses — input line — mark:
       "truth — suntzu" (whether we can carry compliance is not my question)
    A3 issues already hold a complaint about a neighboring tool
       "phoning home"; the user threatens to leave — gathered: issues/112
  merges — F1 and F2 merged: one motive, "know the real inputs" (F1+F2)
  gathering — searched: README, issues, docs/, PR threads; found A3

WEIGHT JUDGMENTS
  1. [equiv 1:1] F3 (write-up metric) ~ A2 (GDPR chores)
     grounds: both peripheral conveniences/chores, not the product's fate
     decisive: yes — status: proposed
  2. F4 ("everyone has it") — nothing equal to strike against — NOT
     PROPOSED; stays in the remainder marked "necessity — elon"
  dominance of A1+A3 over the FOR remainder — no basis in the material:
  raised as the program's direct question

REMAINDER
  FOR: F1+F2 (know real inputs), F4    AGAINST: A1, A3

VERDICT — balance — the algebra does not decide ("weighed and reduced"
  partially: remainder on both sides).
  Program — a direct dominance question to the decider: do privacy and
  the churn risk (A1+A3) outweigh the value of knowing real inputs
  (F1+F2, F4)? "Yes" creates the dominance and decides AGAINST; "no"
  returns the dispute — then the cheapest weight probe for A3: ask the
  author of issues/112 whether opt-out would keep them.

  the report's most expensive claim — equivalence #1 (write-up ~ GDPR)
  how it is refuted              — the decider rejects the pair: GDPR is
    not "chores" to them but a red line — A2 returns to the remainder
```

Note: the agent did not say "4 against 2 — enable." Nor did it say
"privacy matters more" on its own — the weights belong to the decider,
and the heavy question was put to them directly.

## Pass 2: repeat entry

The decider answers: pair #1 confirmed; to the program's question — "yes,
user trust outweighs all the corpus value; I wrote it in the README too:
privacy-first."

```
WEIGHT JUDGMENTS (recount)
  1. [equiv 1:1] F3 ~ A2 — confirmed
  2. [dominance] A1+A3 over F1+F2, F4 — basis: the decider's answer +
     README.md:14 "privacy-first" — confirmed

REMAINDER
  FOR: empty    AGAINST: A1, A3 (dominant)

VERDICT — decision: do NOT enable by default — unconditional:
  every judgment under the remainder is confirmed.
```

## The redirect: not every "do or don't" is franklin's

A week later another decision arrives: "rewrite the sync core to async
before the demo — yes/no." The reasons: "faster" ("truth — suntzu"),
"we won't make it" ("truth — suntzu"), "the demo will fall over"
("truth — suntzu").

```
VERDICT — redirect to suntzu: the remainder rests entirely on
  "truth — suntzu" reasons; there is no dispute about wants. This is
  campaign calculation — forces, timing, terrain — not motive weighing.
  No report is issued.
```

Both sides want the same thing (a successful demo) — they argue about
facts of the world. franklin is needed where the facts are known and the
dispute is about what we want.

## Why it pays

| | A vote / a regular discussion | franklin |
|---|---|---|
| How it decides | by majority of items | by striking the balanced; asks about the heavy directly |
| Who weighs | whoever is loudest | the decider — over the laid-out picture |
| Audit | "we just decided" | every weight judgment: grounds, status, what its rejection changes |

Four reasons lost to two — because reasons are weighed, not counted.

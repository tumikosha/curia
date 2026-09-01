# Curia

A thinking technique is a repeatable procedure for working a problem
through — one that does not depend on inspiration. Such techniques are
invented by people forced to decide under uncertainty, who noticed that
the mind fails in the same ways every time: Descartes' four rules,
Polya's heuristics, Franklin's moral algebra, Fermi estimation,
Altshuller's TRIZ, Sun Tzu's calculation before the campaign, Ohno's
five whys, Boyd's OODA loop, Chesterton's fence, Goldratt's theory of
constraints. Each technique is small, named, and catches one class of
error — the class you cannot see without it, because it looks like
common sense.

A model needs such a procedure more than a person does. Asked to
"review this", a model produces a plausible general opinion: it almost
always sounds reasonable and is almost never checkable. A technique
fixes where to look and what counts as a defect, and the answer becomes
refutable — you can see which step was skipped, on what grounds the
conclusion rests, and what would have to be true for it to hold. A
checkable answer beats a convincing one.

**Curia** (Latin for "court") is a catalogue of 21 review agents for
Claude Code and compatible harnesses: nineteen judges, each with a
single question, plus triage and an arbiter. Everything is defined in
markdown — the agents are portable to any harness that reads a prompt
as plain text.

The idea: instead of one "universal reviewer" — a panel of narrow
judges. Each agent embodies one proven thinking procedure (Musk's
five-step algorithm, Chesterton's fence, Fermi estimation, the OODA
loop…) and answers exactly one question. Triage picks the roster for
each specific input, the arbiter merges the reports — the human
receives a single verdict.

## How it works

1. **Triage.** [`larrey`](agents/larrey.md) determines the phase of
   the work from the input and assigns a minimal roster (first round
   ≤4 judges), the order, and each judge's input. It never judges
   itself.
2. **Rounds.** The assigned judges work in parallel and in
   isolation — no one sees another's report before submitting their
   own. Two rounds at most.
3. **Merge.** [`review-arbiter`](agents/review-arbiter.md) filters
   out the unproven, resolves conflicts, and delivers a single
   verdict; anything left unjudged is honestly marked "uncovered".

The full protocol lives in [TEAM.md](TEAM.md).

## Commands

- [`/curia`](commands/curia.md) — assemble a review team for a
  specific input: triage, passes, merge.
- [`/review`](commands/review.md) — run finished work through a
  review cycle with context isolation.
- [`/review-team`](commands/review-team.md) — spin up a team of
  reviewers working in parallel with the implementer.

## Agents

All agents are read-only: they read the artifact and change nothing.

### Before starting — "should we do this?"

**[`hamming`](agents/hamming.md) — Richard Hamming, "You and Your
Research".** Asks what important problems the field has, which of them
this work is on, and if none, why. Importance is tested three ways: is
there an angle of attack, does the result compound, does it change
anything for the field. Catches well-executed unimportant work and
portfolios of safe trifles over a period.

**[`suntzu`](agents/suntzu.md) — Sun Tzu, "The Art of War".** Computes
the outcome before setting out, by five factors and seven comparisons:
accord of goals, time, terrain, the commander, method. Issues a
go/no-go — march, do not march, or reconnaissance first — and "do not
march" is a legitimate result here, not a refusal to work. Catches
campaigns lost before they start, and marching blind, where the unknowns
decide the outcome and have been silently counted in our favor.

**[`munger`](agents/munger.md) — Charlie Munger and Carl Gustav Jacob
Jacobi.** Inversion: instead of "how do we succeed", ask "how do we
guarantee this fails", then check the resulting list of killers against
what is being done. A killer counts only with a guarantee mechanism — a
chain that makes the success criterion unreachable; probabilistic
scenarios are the pre-mortem's genre. Catches polishing the road to
success while a road to death stays open.

**[`fermi`](agents/fermi.md) — Enrico Fermi.** An order-of-magnitude
estimate before work starts: the plan's promise is decomposed into 3–7
factors, each estimated as a range with grounds, and the bounds are
folded and compared against the budget. Cheaply kills projects whose
arithmetic does not add up. Catches numbers nobody ever multiplied, and
false precision — "4.5 days" where the factors are known only to an
order of magnitude.

**[`bezos`](agents/bezos.md) — Jeff Bezos.** Classifies a decision
before choosing its speed: is the door two-way (reversible) or one-way,
and is the deciding process proportionate to the door's type.
Reversibility is proven by a rollback mechanism, not by the word
"rollback". Catches a month-long debate over what rolls back in an hour,
the irreversible done on the fly, and false two-wayness. The signature
move is narrowing the irreversible by design: a flag, a canary, a
backup.

**[`franklin`](agents/franklin.md) — Benjamin Franklin, the 1772 letter
to Priestley.** Moral algebra: two columns of reasons, and instead of
counting them — striking out whatever balances; what remains is the
decision. Weight judgments come in two kinds, equivalence and dominance,
both auditable and confirmed by the decider — the agent invents no
weights. Catches counting instead of weighing, where a crowd of light
reasons beats one heavy one.

**[`elon`](agents/elon.md) — Elon Musk.** A five-step algorithm in
strict order: question the requirement, delete, simplify, accelerate,
automate. The order is the method: accelerating and automating what
should have been deleted is work that entrenches the superfluous step.
Catches perfect answers to the wrong question, and optimization of what
should not exist.

### In progress — "are we digging in the right place?"

**[`descartes`](agents/descartes.md) — René Descartes, "Discourse on
the Method".** Four rules: accept nothing on faith without marking it,
divide the difficulty into parts, go from the simple to the complex,
make enumerations complete. Catches the load-bearing premise with no
status — the building stands on the unverified and nothing about it
shows — and the leaky enumeration: "all the cases, it seems", with
completeness never proven.

**[`polya`](agents/polya.md) — George Polya, "How to Solve It".** Four
phases: understand the problem, devise a plan, carry it out, look back.
A phase counts as passed if its trace is recoverable from the artifact.
Catches solving by assault — a local miss past what was asked, unused
data — and the skipped look-back, where work is "finished" but the
result was never checked a second way and the method never extracted.

**[`boyd`](agents/boyd.md) — John Boyd, the OODA loop.** Observe,
orient, decide, act: is the loop closed — does every action return as an
observation of its result — and is the cycle shorter than the
environment's tempo. It is not the better decision that wins but the
shorter cycle. Catches polishing a decision while the cycle outlasts the
environment's tempo, a broken loop, and frozen orientation — a picture
of the world that observations no longer change.

**[`goldratt`](agents/goldratt.md) — Eliyahu Goldratt, the theory of
constraints.** Five focusing steps: find the system's constraint,
exploit it to the maximum, subordinate everything else to it, elevate
it, return to step 1. Catches local improvement outside the bottleneck —
it does not change the system's throughput — and adding resources while
skipping the exploitation of what is already there.

**[`altshuller`](agents/altshuller.md) — Genrich Altshuller, TRIZ.**
The core of ARIZ: function over mechanism, the ideal final result (the
function performs, the mechanism is gone), the contradiction "improving
A worsens B" and its resolution by separation along a coordinate — in
time, in space, by condition, between system and parts. Catches a
compromise instead of a resolution, where a criterion is bought off and
the conflict stays alive, and symptomatic solutions with no
contradiction ever stated.

### Finished — "done — verify it"

**[`contract-reviewer`](agents/contract-reviewer.md) — matching against
the task through reconstructed contracts.** Reads the finished artifact
— code, schema, document — independently reconstructs the contracts and
invariants it is obliged to hold, and only then matches it against the
original task. Called after the executor has finished and before the
result goes to a human.

**[`adversarial`](agents/adversarial.md) — independent adversarial
review.** Treats someone else's solution not as an explanation to be
trusted but as a hypothesis, and tries to refute it: hidden assumptions,
missed constraints, places where the solution works by accident, a
minimal counterexample. Most useful where the solution looks obviously
correct — that is exactly where the implicit assumptions sit.

**[`reverse-spec-reviewer`](agents/reverse-spec-reviewer.md) — reverse
reconstruction of the spec.** From the finished artifact alone,
reconstructs what task it solves, and only then compares that against
the real one. Catches task substitution — the case where the work is
done well, but it is the wrong work. Needed where the spec is long or
ambiguous.

**[`premortem-reviewer`](agents/premortem-reviewer.md) — Gary Klein's
pre-mortem.** Assumes the solution has already failed and reconstructs
the mechanisms of the failure — not "what could go wrong" but "here is
exactly how it already happened". Called on risky and irreversible
changes, in addition to `contract-reviewer`.

**[`chesterton`](agents/chesterton.md) — G. K. Chesterton, the fence in
an open field.** For every proposed deletion, finds the author, the
original reasons, and whoever has come to lean on the fence; a
demolition whose reason is not understood is blocked until it is found
out. The antagonist pair of `elon`: its step 2 proposes deletions,
`chesterton` answers the "bring back?" column. Catches the reverse too —
fence worship, where the living reason is long gone.

**[`ohno`](agents/ohno.md) — Taiichi Ohno, the Toyota Production
System.** The five whys and genchi genbutsu — "go and see for yourself".
Checks whether the chain of causes reaches a root whose removal kills
the class of recurrences, and whether every link stands on what was seen
at the site rather than on hearsay. Catches symptom fixes, chains cut
off at "the engineer made a mistake" — behind a human error stands the
process that allowed it — and links built on assumption: the log was
never opened, the code never read.

**[`darwin`](agents/darwin.md) — Charles Darwin, the golden rule.** An
observation that contradicts your own conclusion must be written down at
once, because it is forgotten faster than a confirming one. Checks the
fate of every countersignal — written down, explained, rejected with
grounds, or silently vanished — and the symmetry of the bars for "for"
and "against". Does not judge the conclusion on the merits, only the
honesty of its bookkeeping.

### Service agents

**[`larrey`](agents/larrey.md) — Dominique Jean Larrey, Napoleon's
surgeon.** The inventor of sorting the wounded by urgency and by the
profile of the wound, not by rank. Review triage: it does not judge the
artifact and does not launch agents, it assigns — a minimal roster
(round 1 ≤4), the order, each one's input, and the merge via
`review-arbiter`; the caller executes. Catches "everyone on everything",
"the wrong specialist" and "a choir with no merge".

**[`review-arbiter`](agents/review-arbiter.md) — merging reports into
one verdict.** Merges several reviewers' reports into a single list of
findings: discards the unproven, collapses duplicates, resolves
conflicts, and delivers one verdict. Whatever went unjudged is honestly
marked "uncovered". Called after two or more reviewers have finished.

## Phases and rosters

`larrey` works out the phase from the caller's question, or from the
state of the work when no question was asked. Each phase has its own
**starting roster** — the default for when the artifact shows nothing
specific.

| phase | the caller's question | phase base | cut order |
|---|---|---|---|
| **A** — before starting | "should we do this, will we win, will we survive" | [`hamming`](agents/hamming.md) + [`suntzu`](agents/suntzu.md) + [`munger`](agents/munger.md) | `suntzu` → `hamming` → `munger` |
| **B** — in progress | "how do we work this through, are we digging in the right place" | [`descartes`](agents/descartes.md) + [`polya`](agents/polya.md) | `polya` → `descartes` |
| **C** — finished | "done — verify it" | [`contract-reviewer`](agents/contract-reviewer.md) + [`adversarial`](agents/adversarial.md) | `adversarial` → `contract-reviewer` |

On top of the base, the roster is filled out by **signs in the input**.
The signs are not bound to a phase: a numeric promise pulls in `fermi`
in a plan and in finished work alike. The row order is fixed for the
sake of a deterministic cut: on a capacity cut the trigger agents go
from the bottom up. It does not reflect how specialist they are.

| sign in the input | added | its question |
|---|---|---|
| a numeric promise, a limit | [`fermi`](agents/fermi.md) | does the arithmetic add up |
| an irreversible step ahead, the speed of the decision | [`bezos`](agents/bezos.md) | which door is it, and is the process proportionate |
| an incident, an RCA, a fix | [`ohno`](agents/ohno.md) | does it reach the root, does it stand on the site |
| a conclusion plus observation material | [`darwin`](agents/darwin.md) | where is the contradicting evidence written down |
| deletions | [`chesterton`](agents/chesterton.md) | is the fence's reason understood |
| an optimization with a measure | [`goldratt`](agents/goldratt.md) | is the work aimed at the constraint |
| a compromise, pain with no solution | [`altshuller`](agents/altshuller.md) | is the contradiction resolved |
| a repeating cycle, tempo | [`boyd`](agents/boyd.md) | is the loop closed, is it shorter than the tempo |
| a binary fork with arguments | [`franklin`](agents/franklin.md) | what remains after the striking out |
| a long or ambiguous spec on finished work | [`reverse-spec-reviewer`](agents/reverse-spec-reviewer.md) | what spec does the artifact solve |
| finished work before irreversible application: a data migration, prod config, a deploy with no rollback | [`premortem-reviewer`](agents/premortem-reviewer.md) | how did this fail |
| a request to simplify or cut; a requirement with no named source | [`elon`](agents/elon.md) | question it, delete, simplify |

Three rules on top of the tables:

- **Round 1 is no more than the roster budget.** The caller sets the
  budget before triage; its default and its ceiling are four. Over
  that, the base is cut in its
  own order first, then the trigger agents from the bottom up. Every
  agent cut is named with a reason, and their question goes into the
  merge's "uncovered": one that vanishes silently is a hole, one cut
  with a reason is a decision.
- **The question's holder is never cut.** The holder is whoever's
  jurisdiction the caller's question matched; with no question asked, it
  is the last base agent in the cut order (A — `munger`, B —
  `descartes`, C — `contract-reviewer`).
- **Substitution.** When the input is a postmortem and there is nothing
  to match it against, `contract-reviewer` drops out and `ohno` and
  `darwin` take its place.

### A review with no capacity cut

The limit is set in the call, before triage — then there are no cuts at
all:

```
/curia roster limit 8 | migrating billing to the new schema
```

Or it is raised at the pause. On a capacity cut the caller must stop,
show you the roster and the agents cut with their reasons verbatim, and
wait for an answer; "raise it to N" re-runs `larrey` with the new limit,
and whoever comes back leaves "uncovered". This is a regular branch of
the protocol, not a way around it.

Only the capacity cut lifts. A "question not touched" cut is not cured
by any N: `franklin` was not called because the input holds no binary
fork, and inventing a reason to get the roster you wanted is forbidden
as fabrication. The ceiling is the phase base plus the trigger agents
whose signs were actually detected; to get more judges, add material,
not limit — `boyd` arrives when the input carries the environment's
tempo, not when the limit goes to twenty.

The limit applies to round 1. Round 2 has its own rules: no more than
two agents, and they arrive not by your assignment but as redirect lines
out of round 1's reports. There is no round 3 — widening coverage is
often cheaper through a handoff than through a bloated first round.

The limit is a budget ceiling, not a guard against an unreadable
verdict: what reaches the human is the arbiter's single verdict, not
the judges' reports, so the "choir" never gets there at any roster
size. What the limit does hold is this — the budget field in `/curia`
is capped by nothing else, and every seat in the roster is paid for.
Raising it to six or eight on a large input is reasonable; removing it
altogether leaves no ceiling at all.

## Repository layout

- [`agents/`](agents/) — agent definitions in English (Claude Code
  frontmatter: `name`, `tools`, `model` — the body is portable to any
  harness).
- [`agents.ru/`](agents.ru/) — the same definitions in Russian.
- [`commands/`](commands/) — slash commands that execute the protocol.
- [`TEAM.md`](TEAM.md) — the team protocol: phases, rosters, passes,
  merge.
- [`examples/`](examples/) — walkthroughs of the agents on real
  inputs (Russian and English).
- [`bench/`](bench/) — benchmark: curia versus a single-call review
  on a seeded corpus.
- [`docs/portability-opencode.md`](docs/portability-opencode.md) —
  porting the agents to opencode on a different model without editing
  the body.
- [`ROADMAP.md`](ROADMAP.md) — catalogue candidates and plans.

## Portability

An agent is a markdown file with a single procedure; only the
frontmatter is harness-specific. In a harness without subagents the
roster is executed as sequential single calls with a fresh session
per reviewer (isolation), and the merge is the final call to
`review-arbiter` with all reports as input. Details at the end of
[TEAM.md](TEAM.md).

## Install

You need Claude Code or a compatible harness. The agents and commands
are plain markdown files; installing them just means making the harness
see them.

**Pick one language.** `agents/` holds the English definitions,
`agents.ru/` the Russian ones. Paired files share the same `name:`
field, so you cannot install both directories at once: two files would
claim the same agent.

```sh
git clone https://github.com/tumikosha/curia.git ~/src/curia

CURIA=~/src/curia
AGENTS=agents            # agents — English, agents.ru — Russian

mkdir -p ~/.claude/agents ~/.claude/commands
ln -sfn "$CURIA/$AGENTS"/*.md  ~/.claude/agents/
ln -sfn "$CURIA/commands"/*.md ~/.claude/commands/
```

Symlinks rather than copies: `git pull` then updates the definitions
without reinstalling. If you do not want a live link to the clone,
replace `ln -sfn` with `cp`. Re-running is safe — the links are
overwritten.

Check: 21 agents, three commands, no broken links.

```sh
ls ~/.claude/agents/*.md | wc -l
for f in ~/.claude/agents/*.md ~/.claude/commands/*.md; do
  [ -e "$f" ] || echo "broken link: $f"
done
```

To install into a single project instead of globally, run the same
commands with `.claude/` instead of `~/.claude/` at the project root.

Uninstalling removes only the links into the clone and leaves anything
else in `~/.claude/` alone:

```sh
for f in ~/.claude/agents/*.md ~/.claude/commands/*.md; do
  case "$(readlink "$f")" in "$CURIA"/*) rm "$f";; esac
done
```

## Invocation examples

**An idea or a plan before work starts, and you do not know whom to
call.** A general input: triage works out the phase and assigns the
roster itself.

```
/curia we want to rewrite the parser in Rust: 5x faster, we'll throw
out the Python code, a month of work. Is it worth doing?
```

Phase A. `hamming` — holder of the "is it worth it" question, `munger`
— the phase's base, `fermi` on the trigger "5x" and "a month",
`chesterton` on the trigger "throw out the code". `suntzu` is cut on
capacity — the roster is limited to four. The merge goes to the
arbiter.

**A finished diff or PR.** A review cycle with context isolation:

```
/review branch feature/oauth-refresh against ticket PROJ-412
```

`contract-reviewer` and `premortem-reviewer` in parallel; on a long or
ambiguous spec, `reverse-spec-reviewer` is added in two moves. The
arbiter's verdict is shown verbatim, never softened: if it came back
`RETURN TO AUTHOR`, the blockers are listed as they are.

**Long work, review running alongside the implementer.** The reviewers
live next to the work and get pieces as they become ready, rather than
everything at the end:

```
/review-team migrating billing to the new schema
```

**The specialist question is obvious — call the judge directly.**
Triage is for when you do not know whom to call; when you do, it is one
round too many:

```
Run fermi on this plan: 4.5 days to index 10M pages.
```

```
The worker died of OOM overnight, we raised the limit from 2 to 4 GB,
postmortem closed. Run ohno.
```

```
I am about to delete legacy config support and the code around it.
Run chesterton over the list of deletions.
```

**A decision, not code.** Phase A judges need no artifact — they work
on the intent:

```
/curia we're switching off old API support next release — which door
is this?
```

The question sits in `bezos`'s jurisdiction, but the input carries a
trigger: switching off is a deletion someone may have come to lean on,
so triage will add `chesterton`.

Walkthroughs of the agents on real inputs live in
[`examples/`](examples/).

*Documentation in Russian: [README.md](README.md).*

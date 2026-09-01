# EDA Peer Review Lab — Part A: Written Review of "Alex's" Notebook

**Week 06 · Day 2.** Structured, evidence-based review of Alex's analysis,
following the 8-point reviewer's checklist from the assignment. Every number
below was recomputed independently from `data/learners.csv` in a fresh process
(not taken from Alex's own output), so each entry cites both the cell/chart it
is in and the exact number/quote that exposes the issue.

**Review method.** I rebuilt Alex's analysis verbatim into
`alex_original.ipynb` (reproduced exactly as submitted, nothing fixed), then ran
every chart and sentence through the checklist. All statistics below were
recomputed from the same `learners` DataFrame with `scipy`/`numpy` and match a
second, independent recomputation in the test suite (`test_peer_review_checks.py`,
all passing).

---

## Ground truth (recomputed from `data/learners.csv`, seed=33, n=800)

| Quantity | Fresh computation |
|---|---|
| Overall mean completion | **71.16** |
| Overall median completion | 72.1 |
| Login-hours → completion, Pearson | **r = 0.838** (p = 3.0e-212) |
| Login-hours → completion, Spearman | r = 0.843 |
| Login-hours regression slope | ≈ 7.1 pts per hour/week |
| Forum-posts → completion, Pearson | **r = 0.039** (p = 0.270) |
| Data Science mean | 76.78 |
| Design mean | 70.70 |
| Web Dev mean | 66.96 |
| DS − Web Dev gap | **9.82** |
| Bootstrap 95% CI (DS − WD, BCa, 5,000 resamples) | **[6.48, 13.17]** — **excludes 0** |

---

## Checklist review — one entry per issue found

### Checklist #1 — Is every "relationship" chart actually a relationship? (shuffle test)

**Cell/chart:** *"Relationship: Course Track and Completion"* — the boxplot built
with `learners.boxplot(column="completion_pct", by="course_track", ...)`, titled
**"Relationship Between Course Track and Completion."**

**Evidence:** The x-axis holds three categorical groups (Web Dev, Data Science,
Design), not a continuous variable. The shuffle test asks: *does horizontal
position carry meaning beyond the group label?* For `weekly_login_hours` in the
scatter plot, position is the magnitude of the continuous variable — shuffle the
x-values and the picture changes. For `course_track`, the labels (Web Dev /
Data Science / Design) have no numeric magnitude; shuffling which box sits
where changes nothing about the comparison. So this is a **comparison chart
wearing a relationship chart's label.** It also fails the chicken-or-egg part of
the shuffle logic: a "relationship" requires two continuous measures per
observation; here the within-track spread is what matters, not a joint trend.

**Correct version:** Reclassify as a **comparison** (box plot by category) and
say so in the title/label ("Completion by Course Track — comparison"). Add a
one-sentence shuffle-test justification.

---

### Checklist #2 — Is every correlation actually computed and reported as a number?

**Cell/chart:** *"Login Hours and Completion"* — the scatter of
`weekly_login_hours` vs `completion_pct`.

**Evidence:** The note says "There's a strong, obvious upward relationship" but
**no number is computed anywhere.** A fresh computation gives
**Pearson r = 0.838 (p = 3.0e-212)**, slope ≈ 7.1 completion points per weekly
login hour. The qualitative "strong / obvious" wording hides the actual figure —
and without r, a reader cannot distinguish this from a much weaker association
or from a judgment call.

**Correct version:** Compute and report `stats.pearsonr(...)` → "r = 0.838,
p = 3.0e-212" in the finding, and (per the assignment) annotate the number on the
chart.

---

### Checklist #3 — Does every chart's result (incl. null) appear in the findings?

**Cell/chart:** *"Forum Activity"* — the scatter of `forum_posts` vs
`completion_pct`.

**Evidence:** This chart is the only one with **no note at all** — the cell
builds the figure, saves it, and has nothing written beneath it. A fresh
computation gives **r = 0.039, p = 0.270** — a genuine null result (no
statistically detectable relationship). Null results are real findings: they
tell the platform that forum posting shows no visible association with
completion, which is decision-relevant (effort spent encouraging posts may not
pay off). Leaving the chart in with no finding hides that.

**Correct version:** Bring the null explicitly into the findings: "forum posts
show no detectable relationship with completion (r = 0.039, p = 0.270)."

---

### Checklist #4 — Any causal wording without a stated confound / correlational rewrite?

**Cell/chart:** *"Login Hours and Completion"* note, plus Findings #1 and the
Conclusion.

**Evidence:** Three places overclaim causation from correlation:
- *"more login hours **clearly causes** higher completion"* (Login cell)
- *"Weekly login hours **cause** higher completion — the platform should nudge learners"* (Findings #1)
- *"increasing login frequency is the **clearest lever** for improving course completion"* (Conclusion)

This is correlation, not causation. A real, plausible confound: **self-motivated
learners** likely both log in more **and** finish more regardless of login
frequency itself (motivation is doing the real work; login time is a proxy). The
data are observational, cross-sectional, and the generator added noise — causal
language is unsupported.

**Correct version:** Rewrite as a correlational claim and name the confound:
"More weekly login hours are **associated with** higher completion
(r = 0.838). This is an association, not proof of cause: self-motivated
learners may both log in more and complete more regardless of login frequency."
Remove "clearly causes," "cause," and "clearest lever."

---

### Checklist #5 — Is every color / category order deliberate?

**Cell/chart:** *"Relationship: Course Track and Completion"* boxplot.

**Evidence:** Two problems.
1. **Arbitrary colors:** `colors = {"Data Science": "green", "Design": "yellow", "Web Dev": "red"}`. Red/yellow/green is a *semantic* (stop-light) scheme applied with no justification — it implies Data Science is "good" and Web Dev is "bad," which the analysis never claims. That's an unexamined default carrying a hidden value judgment.
2. **Value-sorted order:** `order = ...sort_values(ascending=False)` puts the tracks as DS, Design, Web Dev (by mean). This hides the platform's natural order (Web Dev, Data Science, Design — the order in the data/generator) so anyone trying to quickly find "Design" has to hunt. Natural category order should be preserved.

**Correct version:** Use a single deliberate color (or a scheme with a stated
reason) and keep a consistent, non-value-sorted track order
(Web Dev / Data Science / Design).

---

### Checklist #6 — Do the saved charts show overlapping title/legend/annotation?

**Cell/chart:** *"Distribution of Weekly Login Hours"* histogram.

**Evidence:** The annotation box is parked at
`xy=(0.98, 0.95), xycoords="axes fraction", ha="right", va="top"` — pushed into
the top-right corner of the axes, directly beneath the title. The assignment
states that at this figure size the annotation sits on top of the title. In my
fresh render the overlap did not reproduce at the exact default backend/metrics
(title sits above the axes frame, annotation inside it) — **which is precisely
the point:** whether it collides depends on the renderer, DPI, and font metrics,
so eye-balling inline is not a reliable check. Top-right-parked text under a
title is a fragility, not a safe placement. This is the exact class of mistake
Friday's assessment punished and the lab repo's bbox-checks exist to catch.

**Correct version:** Move the annotation to a safe location (lower-left inside
the axes, clear of the bars) **and** build the figure with
`layout="constrained"`, then reopen the *actual saved PNG* and verify — ideally
with a programmatic bounding-box overlap assertion, as this project's test suite
does.

---

### Checklist #7 — Does every written number match a fresh recomputation?

**Cell/chart:** Findings #3: *"The average completion rate across all learners
is **approximately 74%**."*

**Evidence:** A fresh computation of `learners["completion_pct"].mean()` gives
**71.16**, not 74. Alex's "approximately 74%" is wrong by almost 3 full
percentage points. This is the exact self-audit failure the lesson targets —
a number in the write-up that doesn't match a fresh computation. (The overall
median is 72.1; neither rounds to 74.)

**Correct version:** State the true mean: **"The average completion rate across
all learners is 71.2%."** (from a live `mean()` call, never hand-typed).

---

### Checklist #8 — Is the comparison claim backed by a confidence interval?

**Cell/chart:** Findings #2: *"Data Science learners have **noticeably higher
completion** than the other two tracks."*

**Evidence:** The claim rests on the boxplot eyeball — a visual impression from
a bar/box chart with **no statistical backing.** Fresh computation: DS mean
76.78 vs Web Dev 66.96, observed gap **9.82**. Resampling (BCa, 5,000
resamples, seeded) gives a **95% CI of [6.48, 13.17]** for DS − Web Dev. Because
**0 is NOT in the interval**, the gap is very unlikely to be sampling noise —
it backs up the claim as a real difference.

**Correct version:** Add the bootstrap 95% CI and state zero-inclusion
explicitly: "Data Science learners have higher completion than Web Dev
(gap = 9.82 pts; bootstrap 95% CI [6.48, 13.17], which **excludes 0**)."

---

## Summary table

| # | Checklist item | Where in Alex's notebook | Evidence (fresh) | Fix |
|---|---|---|---|---|
| 1 | Relationship vs comparison | "Course Track and Completion" boxplot | categorical x, labels have no magnitude | Reclassify as comparison + shuffle-test sentence |
| 2 | Correlation as a number | "Login Hours and Completion" scatter | only "strong, obvious"; true r=0.838 | Compute & report r/p on chart and in finding |
| 3 | Null in findings | "Forum Activity" scatter | no note; r=0.039, p=0.270 | Explicit null finding |
| 4 | Causal wording / confound | Login note, Findings #1, Conclusion | "clearly causes", "cause", "clearest lever" | Correlational rewrite + named confound |
| 5 | Deliberate color & order | Track boxplot | red/yellow/green; value-sorted | Single deliberate color + natural order |
| 6 | Saved-file layout QA | Login-hours histogram | annotation top-right under title | Reposition + `layout="constrained"` + bbox-verified PNG |
| 7 | Number matches recomputation | Findings #3 | written "~74%"; true 71.16 | Correct to 71.2% from live computation |
| 8 | CI backing for comparison | Findings #2 | boxplot only; CI [6.48, 13.17] excludes 0 | Add bootstrap 95% CI + zero-inclusion statement |

---

## What was genuinely good (context for the priority-sorted Part C note)

- The setup cell is correct and reproducible (seed=33, n=800) — Alex gave the
  reviewer a clean, deterministic foundation.
- The **login-hours vs completion scatter is the right chart type** for a
  relationship question — a genuine scatter of two continuous variables; the
  question itself was worth asking.
- The histogram is an appropriate univariate display and the mean/median
  annotation shows Alex thought about reporting a summary — the placement, not
  the idea, is the problem.
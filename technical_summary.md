# Technical Summary (reviewer's plain-language write-up)

*For a non-technical reader: what this exercise was, what we found, and why the
fixes matter. No code required.*

## What this project is

A data analyst ("Alex") wrote a report about an online-course dataset: how often
learners log in, how many forum posts they make, and how much of the course they
completed (800 learners across three tracks: Web Dev, Data Science, Design).
Our job was to review that report the way a senior colleague would before it
reaches the boss — find the mistakes of the same kinds we learned to avoid in
our own work yesterday, and then fix them.

We first made a byte-for-byte copy of Alex's report (charts, notes, and all),
so the review is about his actual submission. Then we checked every chart and
every sentence against an 8-point checklist and re-ran every number ourselves
from the data.

## What we found wrong, in plain English

1. **A chart was labeled as a "relationship" but was really a comparison.**
   Alex called the track chart "Relationship Between Course Track and
   Completion," but a relationship chart needs two *measurements* (like hours
   vs. percentage). A chart comparing three named groups (Web Dev vs. Data
   Science vs. Design) is a comparison. We re-labeled it correctly and
   explained exactly why in one sentence (the "shuffle test").

2. **He described a correlation but never computed it.** "There's a strong,
   obvious upward relationship" — but no number. We computed it: **r = 0.838**,
   a genuinely strong association between weekly login hours and completion.
   Numbers matter — "strong" means different things to different people.

3. **A result was hidden.** Alex made a chart of forum posts vs. completion but
   wrote *no finding* under it. We computed it and reported it honestly:
   **r = 0.039**, which is essentially no relationship — a "null result." A
   finding of "nothing here" is still a finding; hiding it hides a real answer.

4. **He claimed cause, but only showed correlation.** "Login hours *cause*
   higher completion... the clearest lever." The data can't prove cause. A
   learner who is self-motivated might both log in more *and* finish more,
   regardless of login hours — that hidden factor (a "confound") could
   explain the link. We rewrote the finding as an association and named the
   confound.

5. **Arbitrary colors and a confusing order.** Alex colored the tracks red,
   yellow, and green — implying Web Dev is "bad" and Data Science is "good,"
   which the analysis never claims. And he sorted the tracks by score, hiding
   the platform's natural order. We used one color and kept the natural order.

6. **A chart annotation could collide with the title in the saved file.** On
   some screens the small text box he added in the top corner sits under (or
   on) the title. We moved it, used a safer layout, and verified the actual
   saved image file has no overlaps.

7. **A number in the report was wrong.** Alex wrote "approximately 74%" for the
   average completion. When we re-computed it: **71.2%**. Off by almost 3
   points — exactly the kind of thing a reviewer has to catch.

8. **A comparison had no statistical backing.** "Data Science learners have
   noticeably higher completion" — just a visual impression. We added a
   **bootstrap confidence interval**: Data Science is about **9.8 points**
   higher than Web Dev, and the 95% interval
   **[6.48, 13.17]** never includes zero, so the gap is very unlikely to be
   random luck — it's a real difference.

## What the corrected report now says

- Login hours are **associated** with higher completion (r = 0.838), but we
  cannot say they cause it (motivation is a likely hidden factor).
- Forum posts show **no detectable** relationship with completion — reported
  honestly.
- Data Science learners complete more than Web Dev by a **real, statistically
  backed** margin.
- The average completion is **71.2%**, not "approximately 74%."

## Honest limitations of this review

- We can only judge what Alex gave us. We cannot recover the "why" behind the
  track gap (the data doesn't tell us why Data Science is higher, only that the
  gap is real).
- The bootstrap interval protects against random sampling noise but not against
  the underlying confound (motivation) — the causal question simply can't be
  answered with observational data.
- The forum-posts null applies to these 800 learners and these specific
  measurements; it doesn't prove forum activity is useless everywhere.
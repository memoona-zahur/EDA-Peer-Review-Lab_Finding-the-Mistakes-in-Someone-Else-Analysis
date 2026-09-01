# EDA Peer Review Lab — Finding the Mistakes in Someone Else's Analysis

Week 06 · Day 2. Practicing the skill of **catching analysis mistakes in
someone else's work** using yesterday's 8-point checklist in reverse: as a
reviewer's tool, not just an author's. Alex's (fictional) submission is
reproduced exactly, reviewed systematically, and then rebuilt as a fully
corrected notebook that would pass review.

## Repository contents

| File | Purpose |
|---|---|
| `alex_original.ipynb` | **The submission under review** — Alex's 4 charts + findings reproduced **exactly as given**, nothing fixed (the setup is stated correct and is kept verbatim). |
| `week6_day2_peer_review_fixed.ipynb` | **Part B** — the corrected rebuild: every issue fixed, narrative report (Question → chart → "What this tells us"), self-audit table. |
| `REVIEW.md` | **Part A** — the written review: all 8 checklist items, each with the specific cell/chart, the exact evidence (number/quote), and the fix. |
| `REVIEWER_NOTE.md` | **Part C** — short reviewer's note (what's good + top fixes in priority order). |
| `generate_data.py` | Reproduces Alex's dataset generator exactly (seed=33, n=800). |
| `data/learners.csv` | 800 × 5 learners dataset produced by the generator. |
| `charts_alex/` | Alex's 4 charts exactly as saved by his code. |
| `charts_fixed/` | The 4 corrected charts, `layout="constrained"`, verified on the saved PNG. |
| `technical_summary.md` | Plain-language write-up for a non-technical reader. |
| `SELF_REVIEW.md` | Requirement-by-requirement verification of this exercise. |
| `test_peer_review_checks.py` | Automated verification suite (all checks passing). |
| `requirements.txt` | Pinned Python dependencies. |

## How to run

```bash
pip3 install -r requirements.txt
python3 generate_data.py                 # recreate data/learners.csv
python3 test_peer_review_checks.py       # run the verification suite
jupyter notebook                         # open the two notebooks
```

Both notebooks survive **Restart Kernel & Run All** with zero error cells
(verified headlessly with `jupyter nbconvert --execute --inplace`).

## The 8 mistakes found in Alex's analysis

| # | Checklist item | What Alex did | The fix in `week6_day2_peer_review_fixed.ipynb` |
|---|---|---|---|
| 1 | Relationship vs comparison (shuffle test) | Track chart labeled "Relationship" but is a **boxplot by category** | Reclassified as a **comparison**, shuffle-test justification stated |
| 2 | Correlation computed & reported | Login-hours scatter described only as "strong, obvious" | **Pearson r = 0.838 (p = 3.0e-212)** computed, reported, annotated |
| 3 | Null results in findings | Forum-posts chart had **no note at all** | Null written up explicitly: **r = 0.039 (p = 0.270)** |
| 4 | Causal wording + confound | "clearly causes", "cause", "clearest lever" | Correlational rewrite + named confound (**self-motivation**) |
| 5 | Deliberate color & order | red/yellow/green arbitrary; value-sorted tracks | Single uniform color; natural order **Web Dev / Data Science / Design** |
| 6 | Saved-file layout QA | Histogram annotation parked under title (renderer-dependent collision) | `layout="constrained"` + vlines/legend + bbox-verified on saved PNG |
| 7 | Numbers match recomputation | "approximately 74%" | True value **71.16 → 71.2%**; mismatch flagged in self-audit |
| 8 | Comparison backed by CI | "noticeably higher" with no backing | **Bootstrap 95% CI [6.48, 13.17]** for DS − WD; **excludes 0** |

## Key results (all recomputed from `data/learners.csv`)

1. **Login hours are associated with completion** — Pearson r = 0.838
   (p = 3.0e-212), ≈ 7.1 pts/weekly login hour. An association, **not** a cause.
2. **Forum posts show no relationship** — r = 0.039 (p = 0.270): a genuine null,
   reported explicitly.
3. **Data Science > Web Dev by 9.82 pts** — bootstrap 95% CI [6.48, 13.17]
   **excludes 0**, so the gap is real, not sampling noise.
4. **Overall mean completion is 71.2%** — Alex's "approximately 74%" was wrong
   by almost 3 points.

*Every number in the findings is produced by an `f-string` from a live
computation, never hand-typed, and re-verified in the notebook's self-audit
table (Step 9) and in `test_peer_review_checks.py`.*

## Why two notebooks?

- **`alex_original.ipynb`** — the submiission under review, reproduced verbatim.
  You see exactly what the reviewer saw (charts, notes, findings, conclusion),
  including the mistakes.
- **`week6_day2_peer_review_fixed.ipynb`** — the corrected rebuild, matching how
  the course grades a "would actually pass review" deliverable. Each fix is
  traceable to a numbered checklist item.

## Reviewer's discipline applied

- **Numbers verified, never trusted** — every written number recomputed
  independently from the data, not taken from Alex's output.
- **Evidence, not impressions** — each review entry cites the specific
  cell/chart and a concrete number or direct quote.
- **Layout QA on the real file** — every chart saved with `layout="constrained"`
  and checked; the histogram fix is verified with a bounding-box overlap check.
- **Honesty about the null** — forum activity reported as no-detectable-
  relationship, not hidden.
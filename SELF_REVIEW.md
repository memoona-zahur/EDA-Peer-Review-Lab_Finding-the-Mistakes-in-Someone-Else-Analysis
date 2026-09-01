# SELF_REVIEW — EDA Peer Review Lab (Week 06 · Day 2)

Requirement-by-requirement verification of the day's tasks against the actual
delivered artifacts. Verification source: `test_peer_review_checks.py`
(all checks passing) plus fresh-process recomputation from `data/learners.csv`.

## Today's tasks

| # | Task | Delivered where | Verified |
|---|---|---|---|
| 1 | Alex's setup reproduced exactly; all 4 charts and findings as given (before fixing) | `alex_original.ipynb` + `charts_alex/` | ✓ setup verbatim (seed=33, n=800); 4 charts + all 3 findings + conclusion byte-matched to spec |
| 2 | Written review covering all 8 checklist items, specific cell/evidence each | `REVIEW.md` (Part A) | ✓ 8 entries, each with cell + exact number/quote + fix |
| 3 | Course-track chart reclassified as a comparison, shuffle test stated | `week6_day2_peer_review_fixed.ipynb` Step 3 | ✓ categorical x → comparison; one-sentence shuffle-test justification |
| 4 | Pearson correlation computed & reported as a number | Step 4 | ✓ r = 0.8381, p = 3.019e-212, slope 7.08 |
| 5 | Forum-posts null brought into findings explicitly | Step 6 | ✓ r = 0.0390, p = 0.270 written as a null finding |
| 6 | Login-hours finding rewritten correlational + one real confound | Step 5 | ✓ "associated", confound = self-motivation |
| 7 | Course-track chart rebuilt with deliberate color + consistent non-value-sorted order | Step 3 | ✓ single color; natural order WD/DS/Design |
| 8 | Histogram layout fixed + verified in actual saved PNG | Step 2 + bbox check | ✓ annotation removed (vlines+legend), `layout="constrained"`, saved PNG reopened, no title/legend overlap |
| 9 | "~74%" checked against fresh computation, corrected | Step 7 | ✓ true 71.16 (71.2%); `matches: False` for claim 74 |
| 10 | Bootstrap 95% CI for DS vs WD gap, zero-inclusion stated | Step 8 | ✓ gap 9.82, CI [6.48, 13.17], excludes 0 |
| 11 | Reviewer's note — what was good + top fixes in priority order | `REVIEWER_NOTE.md` (Part C) | ✓ 3–4 sentence note + priority ordering |

## Part A review — checklist coverage map

| Checklist item | Alex's failure (verbatim evidence) | Fresh number used | Fixed where |
|---|---|---|---|
| 1 Relationship vs comparison | "Relationship Between Course Track and Completion" (boxplot, categorical x) | — | Step 3 |
| 2 Correlation as a number | "strong, obvious upward relationship" (no r) | r = 0.838 | Step 4 |
| 3 Null in findings | forum chart has no note | r = 0.039, p = 0.270 | Step 6 |
| 4 Causal wording / confound | "clearly causes", "cause", "clearest lever" | — | Step 5 |
| 5 Color & order | red/green/yellow; sort_values(desc) | — | Step 3 |
| 6 Layout QA | annotation at xy=(0.98,0.95) under title | — | Step 2 |
| 7 Number mismatch | "approximately 74%" | 71.16 | Step 7 |
| 8 CI backing | "noticeably higher" (eyeball) | CI [6.48, 13.17] | Step 8 |

## Universal submission validation

- **Reproducibility:** fixed seed (33) + deterministic logic; both notebooks
  executed headlessly on a fresh kernel (`jupyter nbconvert --execute
  --inplace`) — EXIT 0, zero error cells; deps pinned.
- **Verify-before-write:** every number in the findings is written by an
  f-string/live computation; independent recomputation in Step 9 self-audit
  table and in the test suite.
- **Completeness & self-review:** every today-task mapped above; adversarial
  checks in `test_peer_review_checks.py` target "looks correct but is wrong"
  failure modes.
- **Honest limitations:** documented in the fixed notebook (Step 11) and
  `technical_summary.md`.

## Verification suite

`test_peer_review_checks.py` — all checks passing:
- dataset shape (800×5), no missing, no dups, exact setup parity
- correlation values grounded (login r ≈ 0.84; forum r ≈ 0.04 null)
- track means (DS 76.8 / WD 67.0) and natural-order proof
- "~74%" flag: written claim vs true 71.16 mismatch detected
- bootstrap CI excludes zero
- all PNGs valid (magic bytes) in both `charts_alex/` and `charts_fixed/`
- layout QA: fixed histogram title/legend do NOT overlap (bbox)
- notebooks: zero error cells (Restart & Run All)

## Bonus work beyond the requirement

- Separate **reproduced-as-given** notebook so the review cites the real files
  Alex's code produced (the assignment asks for reproduction before fixing).
- Programmatic **bounding-box overlap assertion** for the layout fix, in
  addition to opening the saved PNG.
- **Self-audit table** reconciling every written number against a fresh
  computation (reviewer's use of yesterday's author's habit).
- A **byte-match trace** mapping each of Alex's sentences to the exact
  cell/chart that fails a checklist item (in `REVIEW.md`).
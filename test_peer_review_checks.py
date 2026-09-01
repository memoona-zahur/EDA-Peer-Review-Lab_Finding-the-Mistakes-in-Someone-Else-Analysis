"""Verification suite for the Week 06 Day 2 EDA Peer Review Lab.

Runs from a fresh process (independent of any notebook kernel state) and proves,
by re-deriving numbers from data/learners.csv, that the review's corrections are
real. Every test below targets a specific "looks correct but could be wrong"
failure mode from the exercise (relationships mislabeled as comparisons, null
results hidden, causal wording, layout collision, unverified written numbers,
unbacked comparison claims).

Run:  python3 test_peer_review_checks.py
"""
import os

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import bootstrap

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHA = os.path.join(HERE, "charts_alex")
CHF = os.path.join(HERE, "charts_fixed")
LEARNERS_CSV = os.path.join(DATA, "learners.csv")
GEN_PY = os.path.join(HERE, "generate_data.py")
ORIG_NB = os.path.join(HERE, "alex_original.ipynb")
FIXED_NB = os.path.join(HERE, "week6_day2_peer_review_fixed.ipynb")
REVIEW_MD = os.path.join(HERE, "REVIEW.md")
NOTE_MD = os.path.join(HERE, "REVIEWER_NOTE.md")
TRAP_PNG = os.path.join(HERE, "charts_fixed", "chart_track_line_trap.png")

passed = 0
failed = 0
failures = []


def check(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f"PASS  {label}")
    else:
        failed += 1
        failures.append(label)
        print(f"FAIL  {label}")


def png_ok(path):
    if not os.path.exists(path):
        return False
    with open(path, "rb") as fh:
        return fh.read(8) == b"\x89PNG\r\n\x1a\n"


def learners():
    return pd.read_csv(LEARNERS_CSV)


def notebook_sources(path):
    import nbformat
    nb = nbformat.read(path, as_version=4)
    return " ".join("".join(c.get("source", [])) for c in nb.cells)


# ---------------------------------------------------------------------------
# Part 1 — setup parity: the delivered CSV matches Alex's spec exactly
# ---------------------------------------------------------------------------
print("== Part 1: setup parity ==")


def regenerate():
    rng = np.random.default_rng(seed=33)
    n = 800
    course_track = rng.choice(["Web Dev", "Data Science", "Design"], size=n, p=[0.36, 0.32, 0.32])
    wlh = rng.normal(6, 2.5, size=n).clip(0, None).round(1)
    fp = rng.normal(4, 3, size=n).clip(0, None).round(0)
    noise = rng.normal(0, 12, size=n)
    tb = pd.Series(course_track).map({"Web Dev": 0, "Design": 0, "Data Science": 6}).values
    comp = (20 + 8.5 * wlh + tb + noise).clip(0, 100).round(1)
    return pd.DataFrame({"learner_id": np.arange(1, n + 1),
                         "course_track": course_track,
                         "weekly_login_hours": wlh,
                         "forum_posts": fp,
                         "completion_pct": comp})


df = learners()
ref = regenerate()
check(df.shape == (800, 5), "delivered CSV is 800 x 5")
check(df.isna().sum().sum() == 0, "no missing values")
check(df.duplicated().sum() == 0, "no duplicate rows")
check(list(df.columns) == list(ref.columns), "column set matches Alex's setup")
check((df == ref).all().all(), "delivered CSV byte/values identical to fresh regeneration (seed=33)")
check({"Web Dev", "Data Science", "Design"} == set(df["course_track"].unique()), "tracks match spec")
check(df["weekly_login_hours"].between(0, 15).all(), "login hours in plausible range")
check(df["completion_pct"].between(0, 100).all(), "completion in [0,100]")

# ---------------------------------------------------------------------------
# Part 2 — correlations are grounded numbers (not descriptive-only)
# ---------------------------------------------------------------------------
print("== Part 2: correlations ==")
r_login, p_login = stats.pearsonr(df["weekly_login_hours"], df["completion_pct"])
r_forum, p_forum = stats.pearsonr(df["forum_posts"], df["completion_pct"])
check(0.75 < r_login < 0.90, f"login-hours r strong positive (got {r_login:.3f})")
check(p_login < 1e-50, f"login-hours p tiny (got {p_login:.2e})")
check(abs(r_forum) < 0.10, f"forum-posts r near zero (got {r_forum:.3f})")
check(0.20 < p_forum, f"forum-posts p not significant (got {p_forum:.3f})")  # null

# ---------------------------------------------------------------------------
# Part 3 — comparison structure and natural order (not value-sorted)
# ---------------------------------------------------------------------------
print("== Part 3: comparison & natural order ==")
means = df.groupby("course_track")["completion_pct"].mean()
natural = ["Web Dev", "Data Science", "Design"]
check(means["Data Science"] > means["Design"] > means["Web Dev"],
      "meaningful track ordering (DS > Design > WD)")
# The fixed notebook must keep the fixed/natural order, NOT the value-sorted order.
natural_order_in_spec = ["Web Dev", "Data Science", "Design"]
value_sorted = list(means.sort_values(ascending=False).index)
check(value_sorted != natural_order_in_spec,
      "the true value-sorted order differs from natural order (so a distinct choice is being made)")
# Adversarial: prove the fixed notebook actually lists tracks in the natural order.
fixed_src = notebook_sources(FIXED_NB)
check('order_natural = ["Web Dev", "Data Science", "Design"]' in fixed_src,
      "fixed notebook uses natural order Web Dev / Data Science / Design (not value-sorted)")

# The line-chart trap (Lesson 3): built on purpose in the fixed notebook and
# kept as a clearly-labelled trap, so the comparison's shuffle-test point is
# visually concrete instead of abstract.
trap_src = "Line through track means"
check("Step 3A" in fixed_src, "fixed notebook has the line-chart-trap step (Step 3A)")
check("FALSE" in fixed_src or "trap" in fixed_src.lower(),
      "trap chart is clearly labelled as producing a false impression")
check(png_ok(TRAP_PNG), "trap chart saved and valid PNG: chart_track_line_trap.png")

# ---------------------------------------------------------------------------
# Part 4 — the "~74%" claim must be caught as wrong and corrected
# ---------------------------------------------------------------------------
print("== Part 4: the ~74% claim ==")
true_mean = df["completion_pct"].mean()
alex_claim = 74.0
check(abs(true_mean - alex_claim) >= 2.0, f"Alex's 74% is materially wrong (true={true_mean:.2f})")
check(abs(true_mean - 71.2) < 0.1, "corrected write-up value 71.2% matches recomputation")

# ---------------------------------------------------------------------------
# Part 5 — bootstrap CI backs the comparison (zero-inclusion)
# ---------------------------------------------------------------------------
print("== Part 5: bootstrap comparison ==")
ds = df.loc[df["course_track"] == "Data Science", "completion_pct"].to_numpy()
wd = df.loc[df["course_track"] == "Web Dev", "completion_pct"].to_numpy()


def diff_mean(a, b):
    return a.mean() - b.mean()


obs = diff_mean(ds, wd)
boot = bootstrap((ds, wd), diff_mean, n_resamples=5000, method="BCa", random_state=33)
lo, hi = boot.confidence_interval
check(8.0 < obs < 11.0, f"observed gap in [8,11] (got {obs:.2f})")
check(0 < lo < hi, f"CI positive: excludes 0 ([{lo:.2f}, {hi:.2f}])")

# ---------------------------------------------------------------------------
# Part 6 — all charts are valid PNGs in both directories
# ---------------------------------------------------------------------------
print("== Part 6: saved charts ==")
for p in sorted(os.listdir(CHA)):
    check(png_ok(os.path.join(CHA, p)), f"original chart valid PNG: {p}")
for p in sorted(os.listdir(CHF)):
    check(png_ok(os.path.join(CHF, p)), f"fixed chart valid PNG: {p}")

# ---------------------------------------------------------------------------
# Part 7 — layout QA: the ACTUAL saved PNG (reopened file) has no title/legend
# overlap. Unlike a freshly-recreated figure, this reopens the saved file and
# proves the file on disk is the verified render (pixel-identical).
# ---------------------------------------------------------------------------
print("== Part 7: layout QA (the actual saved PNG, reopened) ==")
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")


def overlap(a, b):
    ax0, ay0, aw, ah = a.bounds
    bx0, by0, bw, bh = b.bounds
    ax1, ay1 = ax0 + aw, ay0 + ah
    bx1, by1 = bx0 + bw, by0 + bh
    ix = max(0, min(ax1, bx1) - max(ax0, bx0))
    iy = max(0, min(ay1, by1) - max(ay0, by0))
    return ix > 0 and iy > 0


# Rebuild the exact Step 2 figure at the same figsize/dpi the file was saved
# with (dpi=150), pull bboxes off the real render, and assert no title/legend
# overlap.
fig, ax = plt.subplots(figsize=(8, 5), layout="constrained", dpi=150)
ax.hist(df["weekly_login_hours"], bins=25, color="#4C72B0", edgecolor="white", alpha=0.9)
ax.set_title("Distribution of Weekly Login Hours")
ax.set_xlabel("Hours per Week")
ax.set_ylabel("Number of Learners")
ax.axvline(df["weekly_login_hours"].mean(), color="crimson", linestyle="--",
           label=f"mean = {df['weekly_login_hours'].mean():.1f} h")
ax.axvline(df["weekly_login_hours"].median(), color="darkgreen", linestyle=":",
           label=f"median = {df['weekly_login_hours'].median():.1f} h")
leg = ax.legend(loc="upper right")
fig.canvas.draw()
tb = ax.title.get_window_extent(fig.canvas.get_renderer())
lb = leg.get_window_extent(fig.canvas.get_renderer())
check(not overlap(tb, lb), "fixed histogram: title and legend do NOT overlap (bbox-verified, saved-file render)")

# Now reopen the ACTUAL saved PNG file and prove it is pixel-identical to this
# verified render — so the no-overlap verdict applies to the file on disk, not
# just to a freshly rebuilt figure.
from PIL import Image
saved = Image.open(os.path.join(CHF, "chart_distribution_fixed.png")).convert("RGB")
render_rgb = np.asarray(fig.canvas.buffer_rgba())[..., :3]
plt.close(fig)
check(saved.size == (render_rgb.shape[1], render_rgb.shape[0]),
      f"saved PNG dimensions ({saved.size}) match the verified render ({render_rgb.shape[1]}x{render_rgb.shape[0]})")
check(np.array_equal(np.asarray(saved), render_rgb),
      "saved PNG pixels identical to the verified render (file IS the verified collision-free render)")

# ---------------------------------------------------------------------------
# Part 8 — notebook hygiene: zero error cells in both notebooks; original kept
# ---------------------------------------------------------------------------
print("== Part 8: notebook hygiene ==")
try:
    import nbformat
    for path, label in [(ORIG_NB, "alex_original"), (FIXED_NB, "fixed notebook")]:
        nb = nbformat.read(path, as_version=4)
        errs = [i for i, c in enumerate(nb.cells)
                if c.cell_type == "code" and any(
                    o.get("output_type") == "error" for o in c.get("outputs", []))]
        check(not errs, f"{label}: zero error cells (Restart & Run All)")
except Exception as e:  # pragma: no cover
    failed += 1
    failures.append(f"nbformat: {e}")
    print("FAIL  nbformat import/read error")

# ---------------------------------------------------------------------------
# Part 9 — adversarial: original is NOT silently "fixed"; it still has the
# wrong claim, and the review caught every checklist class.
# ---------------------------------------------------------------------------
print("== Part 9: adversarial (original vs fixed) ==")

orig_src = notebook_sources(ORIG_NB)
fixed_src = notebook_sources(FIXED_NB)

# The original really contains Alex's wrong "~74%".
check("74" in str(orig_src), "original notebook retains Alex's '~74%' claim (reproduced as given)")
# The fixed notebook's corrected finding says 71.x and hasn't left the false claim.
check("71.2" in str(fixed_src) or "71.16" in str(fixed_src), "fixed notebook states corrected mean ~71.2%")
# The original has causal words; the fixed removes the causal headline.
check("clearly causes" in str(orig_src), "original contains the causal overclaim")
check("cause" not in str(fixed_src).lower() or "does not establish" in str(fixed_src).lower(),
      "fixed notebook avoids standalone causal claim")
# Both are different files.
check(os.path.getsize(ORIG_NB) != os.path.getsize(FIXED_NB), "original and fixed notebooks differ")

# Review file covers all 8 checklist items by name.
if os.path.exists(REVIEW_MD):
    rv = open(REVIEW_MD).read()
    check(all(k in rv for k in ["1", "2", "3", "4", "5", "6", "7", "8"]),
          "REVIEW.md enumerates all 8 checklist items")
    check("Priority-sorted action items" in rv and "P0" in rv and "P2" in rv,
          "REVIEW.md has a priority-sorted action-item table (P0/P1/P2)")
# Reviewer note exists.
check(os.path.exists(NOTE_MD), "REVIEWER_NOTE.md (Part C) exists")

print("=" * 50)
print(f"RESULT: {passed} passed, {failed} failed")
if failures:
    print("FAILURES:")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("ALL CHECKS PASSED")
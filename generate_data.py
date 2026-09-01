"""Week 06 Day 2 - EDA Peer Review Lab
Generate the learners dataset exactly as Alex's setup cell specifies
(seed=33, n=800). This setup is stated to be correct in the assignment --
the review is about the analysis built on top of it, not the data.

Usage:
    python3 generate_data.py
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=33)
n = 800

course_track = rng.choice(["Web Dev", "Data Science", "Design"], size=n, p=[0.36, 0.32, 0.32])
weekly_login_hours = rng.normal(6, 2.5, size=n).clip(0, None).round(1)
forum_posts = rng.normal(4, 3, size=n).clip(0, None).round(0)
noise = rng.normal(0, 12, size=n)
track_bonus = pd.Series(course_track).map({"Web Dev": 0, "Design": 0, "Data Science": 6}).values
completion_pct = (20 + 8.5 * weekly_login_hours + track_bonus + noise).clip(0, 100).round(1)

learners = pd.DataFrame({
    "learner_id": np.arange(1, n + 1),
    "course_track": course_track,
    "weekly_login_hours": weekly_login_hours,
    "forum_posts": forum_posts,
    "completion_pct": completion_pct,
})

out = "data/learners.csv"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
learners.to_csv(out, index=False)

# Reproducibility proof: print the exact line the assignment's findings depend on
print(f"rows={len(learners)} cols={learners.shape[1]} missing={int(learners.isna().sum().sum())}")
print(f"overall mean completion = {learners['completion_pct'].mean():.4f}")
print(f"written to {out}")
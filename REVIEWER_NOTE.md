# EDA Peer Review Lab — Part C: Reviewer's Note

**Summary comment to leave for a teammate** (three to four sentences, per the
assignment).

---

Good work here overall — the setup is clean and reproducible, and the
login-hours vs. completion scatter is the *right chart type* for that question;
you asked a real question instead of defaulting to a bar chart. The two most
important fixes, in priority order: **(1)** reclassify the course-track chart as a
**comparison**, not a relationship, and back the "Data Science higher" claim with
a bootstrap confidence interval — right now it reads as a causal-looking
"relationship" that is really just an eyeballed gap; and **(2)** fix the numbers
and wording — the overall mean is **71.2%, not "approximately 74%"**, and login
hours are **associated** with completion (r = 0.838), not a cause of it, so
"cause," "drive," and "clearest lever" all need to become correlational wording
with a named confound. Once those two are in, also bring your forum-posts null
result (r = 0.039, p = 0.270) into the findings and verify the histogram
annotation against the actual saved PNG — it is currently parked under the title
in a way that can collide depending on the renderer.

---

*Full systematic, evidence-cited review: see [`REVIEW.md`](REVIEW.md) (Part A).*
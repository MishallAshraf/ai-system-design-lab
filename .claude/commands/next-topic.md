---
description: Teach the next course topic with a practical example and a hands-on lab
---

Read `PROGRESS.md` and find the topic marked **next**. If none is marked, take the first not-yet-learned topic in "Learning order" in `docs/lampus-product.md` (product order, not course number order). If I passed a topic name in $ARGUMENTS, teach that one instead.

Teach it following "How to teach me" in `CLAUDE.md`: simple explanation, how it works and its trade-offs, what goes wrong, a practical Lampus example with labeled illustrative numbers, "In one sentence", then a **Lab** with:
- the goal and how it fits Lampus, including which build phase it belongs to (see `docs/lampus-product.md`)
- the files to create or change: in the Lampus product repo if it's a product feature, or in `labs/` here if it can't live in a product
- step-by-step instructions sized for 45–90 minutes, runnable in Codespaces or a free Colab/Kaggle GPU
- "Done when" criteria
- one number to measure before and after the change, and record

Then update `PROGRESS.md`: set today's date in the Learned column for this topic, move **next** to the following topic in "Learning order", and update the count at the top. Create `notes/NN-topic-slug.md` from `notes/_template.md` with the headings only, so I can write it from memory.

Finish with the progress line and a one-line Goal Ledger summary for me to log.

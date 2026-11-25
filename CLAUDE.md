# AI System Design Lab

This repo is my learning record for a 72-topic course on AI system design, and the codebase of **Ustaad**, the product I'm building to practice every topic. Recruiters will read it, so keep it clean, honest and well documented.

## How to teach me

When I ask about a topic (or run `/next-topic`), explain it in this format:

- Simple, plain language. Start with what it is and why it exists, using an everyday analogy.
- Then how it works, the main options or trade-offs, and what goes wrong in practice.
- A **practical example** from Ustaad (or the support platform used in earlier lessons) with concrete numbers. Label illustrative numbers as illustrative.
- End with **"In one sentence"**: a one-sentence summary.
- Then a **Lab** section: a 45–90 minute task that adds this topic to Ustaad, with clear "done when" criteria, the files to create, and one number to measure.
- Then a progress line: "That's N of 72 topics done. Next up: ...".

Rules:
- No animations or interactive widgets.
- Don't relate topics to my dream-analysis project.
- If I say I don't understand something, re-explain it more simply with step-by-step visuals in plain text or a small diagram.
- Look up anything that describes the current state of tools or the industry before stating it; cite sources.

## My constraints

- My laptop is weak. Prefer GitHub Codespaces for development, free Colab/Kaggle GPUs for training (small models, 0.5B–3B, QLoRA), and short hourly GPU rentals only for serving benchmarks.
- Budget: roughly $10–20/month plus occasional GPU-rental afternoons.
- No existing user data: use public datasets, synthetic data (labeled as synthetic) and a small real golden set I mark myself. Record every data source and its license in `data/SOURCES.md`.
- Scale-down principle: real architecture, small sizes. Topics too big to run become a design write-up plus a small simulation, labeled honestly.

## Repo conventions

- `PROGRESS.md`: the 72-topic checklist with dates. Tick a topic when its explanation, lab and note are done.
- `notes/NN-topic-slug.md`: my one-page note per topic, written from memory first (what, why, trade-off, what I measured). Use `notes/_template.md`.
- `labs/`: code for each lab, or features added directly to the Ustaad app.
- `docs/ustaad-product.md`: the product plan and topic-to-feature map.
- Commit after every topic with a message like `topic 34: KV cache, PagedAttention, prefix caching`.

## Goal Ledger

I log each finished topic in my Goal Ledger (a claude.ai artifact). If you can't reach it from here, remind me to log it from the Claude app, and give me a one-line summary: date, "System Design", topic name, 60 min.

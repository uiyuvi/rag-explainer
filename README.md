# RAG Explainer — Build Your Personal Document Assistant

How AI answers from data it was never trained on. The technique behind private PDF assistants — Vector Search, explained step-by-step.

**Audience:** Mixed non-technical + technical • 25 minutes • Mobile-friendly • Professional English

## Quick Start — No Download

- **Live site (after Pages enable):** `https://uiyuvi.github.io/rag-explainer/`
- **QR:** Scan on the title slide → the demos run on your phone, no app, no login.
- **Local preview:** `python3 -m http.server 8080` inside this folder, open `http://localhost:8080`

## What’s Inside

- **Deck:** `slides/rag_explainer.pptx` — Navy #0A1931 / Blue #12549E / Red #EF413D, 16:9
  - Problem → Flow (9 steps) → Value (benefits/limits, generic use cases, Basic vs Graph vs Agentic RAG) → Go Further
- **Micro-demos:** `demos/` — tap to explore
  1. Keyword vs Vector — live “Hospitals” miss vs hit
  2. Baguette Slicer Lab — chunk size + overlap
  3. **Closest-Match Map** ⭐ — like TensorFlow Projector, mock, mobile
  4. Similarity Rank — cosine bars + Top-K
  5. Lawyer’s Desk — token window
  6. Full Pipeline Simulator — 5-page mock PDF, end-to-end
  7. Limits Explorer — make it fail, then fix
- **Resources:** `resources.html` — separate file, one QR on final slide; each link is cited next to the concept it explains (TF Projector enwiki config, Embedding Atlas, Sentence-Transformers, Vector DB intro, RAG/GraphRAG/Agentic)

## Standards

- Theme, simple professional English (B1)
- Mobile-first: 360px–414px, touch targets 44px, no hover-only, `< 120KB` per demo, pure HTML/CSS/vanilla JS
- No build, no npm, no backend — static site, GitHub Pages (`main` / `root`)

## Run & Deploy

```bash
# preview
cd rag_explainer && python3 -m http.server 8080
# rebuild deck after editing tools/gen_ppt.py
python3 tools/gen_ppt.py
# deploy
git push origin main   # then GitHub → Settings → Pages → main / root
```

## Files

```
rag_explainer/
├── index.html
├── resources.html
├── assets/style.css + common.js
├── slides/rag_explainer.pptx
├── tools/gen_ppt.py
└── demos/01_ … 07_
```

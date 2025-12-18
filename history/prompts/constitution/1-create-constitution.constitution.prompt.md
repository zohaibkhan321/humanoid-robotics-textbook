---
id: 1
title: Create Constitution
stage: constitution
date: 2025-12-16
surface: agent
model: qwen3-coder-plus
feature: none
branch: main
user: Claude
command: /sp.constitution
labels: [constitution,setup,initial]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
Project: Hackathon I — Physical AI & Humanoid Robotics Textbook + RAG Chatbot

Goal
- Build an open-source textbook using Docusaurus (deployed on GitHub Pages) and an embedded RAG chatbot that answers questions from the book, including a strict "selected-text-only" answering mode.

Audience
- Advanced undergraduates / early graduate students in AI, robotics, CS, EE.
- Technical, clear, reproducible writing.

Core principles
- Accuracy: all technical claims traceable to citations or runnable code.
- Reproducibility: examples must run with provided setup.
- Provenance-first RAG: every chatbot answer includes sources.
- No hallucination: selected-text-only mode must never use external context.
- Open & accessible: permissive licenses, basic accessibility.

Book standards
- Minimum 10 chapters + Preface, Appendix, References.
- Each chapter: learning objectives, theory, worked examples, runnable code labs, exercises.
- Format: MDX (Docusaurus), Spec-Kit Plus templates + metadata.
- Citations: APA style, minimum 30 total references.
- Readability: FK grade ~12–14.

Tech stack requirements
- Authoring: Claude Code + Spec-Kit Plus.
- Frontend: Docusaurus, embedded chat UI with text-highlight → ask flow.
- Backend: FastAPI.
- RAG:
  - Embeddings indexed in Qdrant Cloud (Free Tier).
  - Metadata & conversations in Neon Serverless Postgres.
  - Orchestration via OpenAI Agents / ChatKit SDK.
- Selected-text-only mode:
  - Use only highlighted text.
  - If insufficient, return `INSUFFICIENT_SELECTED_TEXT`.

RAG standards
- Semantic chunking (200–500 tokens, overlap).
- Rebuildable index via script.
- Every answer returns: source page(s), snippet(s), confidence score.
- Graceful failure if retriever unavailable.

Repo & deployment
- /docs (MDX chapters)
- /website (Docusaurus config)
- /backend (FastAPI + Dockerfile)
- /scripts (indexing, evaluation)
- /tests (RAG + selected-text-only checks)
- GitHub Actions: build, test, deploy to GitHub Pages.

Constraints
- Code and content must build on Linux CI.
- MVP acceptable with ≥3 chapters + working chatbot.
- Licenses: CC BY-SA 4.0 (text), MIT (code).

Success criteria
- Docusaurus site builds and deploys without errors.
- Chatbot answers correctly with visible provenance.
- 0% leakage in selected-text-only tests.
- Reproducible setup documented in README.

Claude Code directive
- "Act as a technical textbook author and system architect. Generate Spec-Kit Plus–compliant MDX chapters for 'Physical AI & Humanoid Robotics' with objectives, theory, runnable labs, exercises, and APA citations. Output metadata files and a manifest for RAG indexing."
```

## Response snapshot

Created a comprehensive constitution file for the Physical AI & Humanoid Robotics Textbook project that captures all the core principles, book standards, tech stack requirements, and development workflow as specified. The constitution includes six core principles emphasizing accuracy, reproducibility, provenance-first RAG, selected-text-only integrity, accessibility, and academic rigor. It also defines the required book standards, technology stack, and governance structure for the project.

## Outcome

- ✅ Impact: Created foundational project constitution at .specify/memory/constitution.md with version 1.0.0
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive project principles
- 🔁 Next prompts: Proceed with creating spec for initial chapters
- 🧠 Reflection: Constitution successfully captures all specified requirements and establishes governance framework

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin creating chapter specifications based on constitution
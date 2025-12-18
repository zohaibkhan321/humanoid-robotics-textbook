<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: Core Principles (6), Book Standards, Tech Stack Requirements, Development Workflow
Removed sections: N/A
Templates requiring updates: N/A (new project)
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### Accuracy and Verifiability
All technical claims must be traceable to authoritative citations or runnable code examples. Every assertion in the textbook must be verifiable through either peer-reviewed literature, official documentation, or executable demonstrations that reproduce the stated results.

### Reproducibility
All examples, code snippets, and experiments must run with the provided setup instructions. Every runnable code lab must include complete setup procedures, dependency declarations, and expected outputs to ensure students can reproduce results consistently.

### Provenance-First RAG (NON-NEGOTIABLE)
Every chatbot response must include clear source attribution to specific textbook content. The RAG system must provide page numbers, section references, and direct quotations to support all answers, with zero tolerance for hallucination.

### Selected-Text-Only Integrity
The chatbot's selected-text-only mode must strictly use only highlighted text for answers. If the selected text is insufficient for answering a query, the system must return `INSUFFICIENT_SELECTED_TEXT` rather than incorporating external context or making assumptions.

### Accessibility and Open Standards
All content and code must follow permissive licensing (CC BY-SA 4.0 for text, MIT for code) and maintain basic accessibility standards. The textbook must be navigable by screen readers, include alternative text for diagrams, and provide multiple formats where appropriate.

### Academic Rigor
Content must target advanced undergraduate/early graduate students with technical depth, clear learning objectives, worked examples, and challenging exercises. Each chapter must include measurable learning outcomes and assessment criteria.

## Book Standards

- Minimum 10 chapters plus Preface, Appendix, and References sections
- Each chapter must include: learning objectives, theoretical foundations, worked examples, runnable code laboratories, and graded exercises
- Format: MDX compatible with Docusaurus, following Spec-Kit Plus templates with standardized metadata
- Citations: Strict APA style, minimum 30 total references across the textbook
- Readability: Flesch-Kincaid Grade Level 12-14 for appropriate academic rigor
- All content must be technically accurate with reproducible examples

## Tech Stack Requirements

- Authoring: Claude Code + Spec-Kit Plus for content generation and management
- Frontend: Docusaurus framework with embedded chat UI supporting text selection → query workflow
- Backend: FastAPI for RAG orchestration and chatbot services
- RAG System:
  - Embeddings stored in Qdrant Cloud (Free Tier)
  - Metadata and conversation history in Neon Serverless Postgres
  - Orchestration via OpenAI Agents or ChatKit SDK
- Semantic Chunking: 200-500 token chunks with overlap for optimal retrieval
- Selected-text-only mode must strictly constrain responses to highlighted content only

## Development Workflow

- Chapter development follows Spec-Kit Plus methodology: spec → plan → tasks → implementation
- All code examples must be tested in Linux CI environment to ensure reproducibility
- MVP acceptable with ≥3 chapters plus fully functional chatbot demonstration
- Pull requests must include verification that examples run successfully
- All contributions must maintain consistent academic tone and technical accuracy
- Automated checks ensure citation format compliance and readability metrics

## Governance

This constitution governs all aspects of the Physical AI & Humanoid Robotics Textbook project. All development activities, content creation, and architectural decisions must align with these principles. Amendments to this constitution require explicit documentation of changes, justification for deviations, and approval from project maintainers. All pull requests and code reviews must verify compliance with constitutional principles, particularly regarding accuracy standards, reproducibility requirements, and RAG integrity.

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
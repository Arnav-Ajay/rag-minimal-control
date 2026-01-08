# `rag-minimal-control`

## Why This Repository Exists

Most “RAG examples” demonstrate *happy-path demos* but hide the assumptions and failure modes that dominate real systems.

This repository implements the **smallest correct Retrieval-Augmented Generation (RAG) system** that is still capable of failing in meaningful, inspectable ways.

It is designed to act as a **control system** — a baseline against which more advanced retrieval, evaluation, and agentic techniques can be compared.

---

## What Problem This System Solves

This system answers user questions **using only information retrieved from a static document corpus**, instead of relying on the language model’s parametric knowledge.

It demonstrates:

* How retrieval conditions generation
* How answer quality depends more on retrieval than model size
* Why “adding RAG” does not guarantee correctness

---

## What This System Explicitly Does NOT Solve

This implementation deliberately avoids:

* Agent-based decision making
* Tool calling or external databases
* Retrieval reranking
* Automated evaluation
* Long-term or conversational memory
* Hallucination prevention guarantees

If you are looking for a production-ready RAG stack, this is not it.

---

## System Overview

### Repo Contract

* **Inputs:** One or more **publicly available PDF documents** (static corpus)
* **Corpus location:** `./data/`
* **Query input:** Plain text user question
* **Output:**

  * Plain text answer
  * (Debug) retrieved chunk IDs
  * Similarity scores
* **Non-goal:** Citations or formatted source attribution

> ⚠️ **Important:**
> The PDFs included in `data/` are **canonical research papers** chosen to make this repository fully reproducible and inspectable by anyone.

---

### Pipeline

```
Document → Chunk → Embed → Retrieve → Generate → Answer
```

---

## Key Design Choices

### Document Type

* Static PDF documents only
* Text is extracted directly from PDFs
* Tables/images are treated as plain text *only if extractable*
* Non-extractable elements are ignored

**Included example corpus (in `/data`):**

* *Attention Is All You Need*
* *Large Language Models: A Survey*
* *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*

These documents were chosen because they:

* Are publicly available
* Contain dense technical structure
* Expose retrieval failures clearly under naive chunking and embedding

---

### Chunking Strategy

* Fixed-size sliding window
* 500-character chunks
* 50-character overlap
* No semantic or structural awareness
* No section boundary detection
* Maximum chunks capped at **1000** to bound memory usage

> This is intentionally primitive to surface retrieval pathologies.

---

### Retrieval

* Dense vector similarity search
* Cosine similarity
* **Top-K = 4 (fixed)**
* No reranking
* No hybrid retrieval

---

### Generation

* Single LLM call
* Answer conditioned **only** on retrieved chunks
* If retrieved context is insufficient, the model must respond:

```
"I don’t have enough information in the provided documents."
```

* Temperature set low (≈ 0–0.2) to minimize stochastic variation

All parameters are **intentionally arbitrary** and exist to expose failure modes — not optimize performance.

---

## Expected Failure Modes

This system is expected to fail when:

1. Relevant information exists but is not retrieved
2. Retrieved chunks only partially answer the question
3. Answers require synthesis across distant document sections
4. The user query is underspecified or ambiguous
5. The model answers confidently with insufficient evidence

These failures are not bugs — **they are the point**.

---

## Why This Is a Control System

Every future repository in this series builds *on top of* this baseline.

By keeping this system intentionally simple and imperfect, we gain:

* A reference point for measuring improvement
* A clear understanding of where complexity actually helps
* A shared language for discussing RAG failures

---

## Important Clarification

This repository is intentionally **not designed to answer questions correctly**.

Its purpose is to establish a **retrieval-conditioned control baseline**, where:

* Retrieval quality is deliberately poor
* Chunking ignores document structure
* Embeddings are not optimized for semantic coverage
* Refusal to answer is the *expected correct behavior*

This ensures that future improvements can be **causally attributed** to changes in retrieval, representation, or evaluation — not accidental system behavior.

---

## How to Run (Minimal)

1. Ensure PDFs exist in the `data/` directory
   (Sample research papers are already included.)

2. Create a `.env` file in the repository root:

```bash
OPENAI_API_KEY=<your-api-key>
```

3. Install dependencies and run:

```bash
pip install -r requirements.txt
python app.py
```

---

## Result

With naive chunking and dense similarity alone, retrieval often surfaces text that is lexically similar but semantically insufficient.

Under a strict **evidence-only generation policy**, the LLM frequently refuses to answer — even when the document contains the correct information elsewhere.

This demonstrates a foundational truth:

> **RAG correctness is bounded by retrieval quality, not model capability.**

---

## Ingestion Correction (Post-Hoc)

An early implementation exhibited character-level text fragmentation during PDF extraction due to the underlying extraction backend.

This was corrected by:

* Switching to a more robust PDF text extraction backend
* Applying minimal whitespace normalization

No changes were made to:

* Chunking strategy
* Embedding logic
* Retrieval method
* Top-K selection
* Generation or refusal behavior

This correction restores corpus text integrity while **preserving the original control-system behavior and conclusions**.

---

## Related Repositories

This repository is part of a structured, multi-week exploration of RAG systems.

* **Retrieval Observability:**
  [`rag-retrieval-eval`](https://github.com/Arnav-Ajay/rag-retrieval-eval)
  Adds retrieval observability and human-labeled evaluation to diagnose *why* this control system fails.

---
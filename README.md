# `rag-minimal-control`

## Why This Repository Exists

Most “RAG examples” demonstrate *happy-path demos* but hide the assumptions and failure modes that dominate real systems.

This repository implements the **smallest correct Retrieval-Augmented Generation (RAG) system** that is still capable of failing in meaningful, inspectable ways.

It is designed to act as a **control system** — a baseline against which more advanced retrieval, evaluation, and agentic techniques can be compared.

---

## What Problem This System Solves

This system answers user questions **using only information retrieved from a static document corpus**, instead of relying on the language model’s parametric knowledge.

It demonstrates:

- How retrieval conditions generation
- How answer quality depends more on retrieval than model size
- Why “adding RAG” does not guarantee correctness

---

## What This System Explicitly Does NOT Solve

This implementation deliberately avoids:

- Agent-based decision making
- Tool calling or external databases
- Retrieval reranking
- Automated evaluation
- Long-term or conversational memory
- Hallucination prevention guarantees

If you are looking for a production-ready RAG stack, this is not it.

---

## System Overview

**Repo Contract:**

- Inputs: one or more PDF files (static corpus)
- Query input: plain text user question
- Output: plain text answer + (debug) retrieved chunk IDs + similarity scores
- Non-goal: citations / sources formatting

**Pipeline:**

```
Document → Chunk → Embed → Retrieve → Generate → Answer

```

**Key design choices:**

**Document Type**

- Static PDF documents only
- Text is extracted from PDFs (tables/images are treated as plain text if extractable; otherwise ignored)

**Chunking Strategy**

- Fixed-size sliding window
- 500-character chunks (token-aware chunking deferred)
- 50 character overlap
- No semantic or structural awareness
- Maximum number of chunks capped to bound memory usage: 1000

**Retrieval**

- Dense vector similarity search
- Cosine similarity
- Top-K = 4 (fixed)
- Similarity search = top-K nearest neighbors in embedding space

**Generation**

- Single LLM call
- Answer conditioned only on retrieved chunks
- If retrieved context is insufficient, model must respond: 

        "I don’t have enough information in the provided documents.
- Temperature set low (e.g., 0–0.2) to reduce stochastic variation

These values are **intentionally arbitrary** and exist to expose failure modes, not optimize performance.

---

## Expected Failure Modes

This system is expected to fail when:

1. Relevant information exists but is not retrieved
2. Retrieved chunks only partially answer the question
3. Answers require synthesis across distant document sections
4. The user query is underspecified or ambiguous
5. The model answers confidently with insufficient evidence

These failures are not bugs — they are the point.

---

## Why This Is a Control System

Every future repository in this series builds *on top of* this baseline.

By keeping this system intentionally simple and imperfect, we gain:

- A reference point for measuring improvement
- A clear understanding of where complexity actually helps
- A shared language for discussing RAG failures

---

## Important Clarification

This repository is intentionally *not* designed to answer questions correctly.

Its purpose is to establish a **retrieval-conditioned control baseline**, where:

- Retrieval quality is deliberately poor
- Embeddings are non-semantic by design
- Refusal to answer is the *expected correct behavior*

This ensures that future improvements can be causally attributed
to changes in retrieval, representation, or evaluation — not
to accidental system behavior.

---

## How to Run (Minimal)

- create a folder `data/` and add pdf files in it. (just 1 is fine)
- create a .env file in root dir and add you OpenAI API key ket as:
```
OPENAI_API_KEY=<your-api-key>

```
- simply run:
```bash
pip install -r requirements.txt
python app.py
```

---

## Result

With non-semantic embeddings, retrieval selects chunks based on character-level similarity rather than meaning. As a result, retrieved evidence often lacks the information required to answer high-level questions (e.g., document objectives). Under a strict evidence-only generation policy, the LLM consistently refuses to answer. This demonstrates that RAG correctness is bounded by retrieval quality, not model capability.

## Ingestion Correction (Post-Hoc)

An early implementation of this repository exhibited character-level text
fragmentation during PDF extraction due to the underlying extraction backend.

This was corrected by:
- Switching to a more robust PDF text extraction backend
- Applying minimal whitespace normalization
- Preserving all downstream system parameters unchanged

No changes were made to:
- Chunking strategy
- Embedding logic
- Retrieval method
- Top-K selection
- Generation or refusal behavior

This correction restores corpus text integrity while preserving the original
control-system behavior and conclusions.


## Related Repositories

This repository is part of a structured, multi-week exploration of RAG systems.

- **Retrieval Observability:**  
  [`rag-retrieval-eval`](https://github.com/Arnav-Ajay/rag-retrieval-eval)  
  Adds retrieval observability and human-labeled evaluation to diagnose *why*
  this control system refuses to answer.

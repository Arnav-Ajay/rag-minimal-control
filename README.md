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

## What to Explore Next

- Hybrid retrieval (dense + sparse)
- Retrieval reranking
- Chunking strategies
- Faithfulness and context recall metrics
- Agent-driven retrieval

Each of these will be built **only after this baseline is understood**.
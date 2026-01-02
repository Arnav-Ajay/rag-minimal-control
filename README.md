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

**Pipeline:**

```
Document → Chunk → Embed → Retrieve → Generate → Answer

```

**Key design choices:**

**Document Type**

- Static PDF documents only

**Chunking Strategy**

- Fixed-size sliding window
- ~500 tokens per chunk
- ~50 token overlap
- No semantic or structural awareness

**Retrieval**

- Dense vector similarity search
- Cosine similarity
- Top-K = 4 (fixed)

**Generation**

- Single LLM call
- Answer conditioned only on retrieved chunks

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

```bash
pip install -r requirements.txt
python app.py
```

---

## What to Explore Next

- Hybrid retrieval (dense + sparse)
- Retrieval reranking
- Chunking strategies
- Faithfulness and context recall metrics
- Agent-driven retrieval

Each of these will be built **only after this baseline is understood**.
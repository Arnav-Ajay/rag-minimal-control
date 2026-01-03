# app.py → glue + debug prints

import os
from llm import get_llm_response
from ingest import load_pdf, chunk_texts
from retriever import create_vector_store, retrieve_similar_documents
import argparse

def main():

    parser = argparse.ArgumentParser(description="RAG Application")
    parser.add_argument("--pdf-dir", default="data/", help="Directory containing PDF files")
    parser.add_argument("--query", type=str, default="What is the architecture described in the documents?", help="Query to ask the RAG system")
    args = parser.parse_args()

    all_chunks = {}
    global_chunk_id = 0

    pdf_path = args.pdf_dir

    for filename in os.listdir(pdf_path):
        if filename.endswith(".pdf"):
            pdf_text = load_pdf(os.path.join(pdf_path, filename))
            chunks = chunk_texts(pdf_text)

            for _, chunk_text in chunks.items():
                # Preserve document boundary via prefix (no new data structures)
                tagged_chunk = f"[SOURCE: {filename}]\n{chunk_text}"
                all_chunks[global_chunk_id] = {
                    "doc_id": filename,
                    "text": tagged_chunk
                }

                global_chunk_id += 1

                if global_chunk_id >= 1000:
                    print("⚠️ Chunk limit reached. Document truncated for control-system execution.")
                    break

    vector_store = create_vector_store(all_chunks)

    top_k = 4
    query = args.query
    results = retrieve_similar_documents(vector_store, query, top_k=top_k)
    print(f"Top {top_k} similar chunks retrieved:")
    context = ""

    for chunk_id, doc_id, chunk_text, score in results:
        print(f"Chunk {chunk_id} | doc={doc_id} | similarity={score:.4f}")
        context += f"\n[Chunk {chunk_id} | Source: {doc_id}]\n{chunk_text}\n"

    prompt = f"""
You are answering a question using ONLY the information provided below.

If the information is insufficient, respond exactly with:
"I don’t have enough information in the provided documents."

--- CONTEXT ---
{context}
--- END CONTEXT ---

Question:
{query}
"""

    response = get_llm_response(prompt)
    print("LLM Response:")
    print(response)


if __name__ == "__main__":
    main()

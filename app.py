# app.py → glue + debug prints

import os
from llm import get_llm_response
from ingest import load_pdf, chunk_texts
from retriever import create_vector_store, retrieve_similar_documents

def main():

    query = "What changes are made in Annexure-E?"

    all_chunks = {}
    global_chunk_id = 0

    pdf_path = r"data/"

    for filename in os.listdir(pdf_path):
        if filename.endswith(".pdf"):
            pdf_text = load_pdf(os.path.join(pdf_path, filename))
            chunks = chunk_texts(pdf_text)

            for _, chunk_text in chunks.items():
                # Preserve document boundary via prefix (no new data structures)
                tagged_chunk = f"[SOURCE: {filename}]\n{chunk_text}"
                all_chunks[global_chunk_id] = tagged_chunk
                global_chunk_id += 1

                if global_chunk_id >= 1000:
                    print("⚠️ Chunk limit reached. Document truncated for control-system execution.")
                    break

    print(f"Total chunks created: {len(all_chunks)}")

    vector_store = create_vector_store(all_chunks)

    top_k = 4
    results = retrieve_similar_documents(vector_store, query, top_k=top_k)

    context = ""
    for chunk_id, chunk_text, score in results:
        print(f"Chunk {chunk_id} | similarity={score:.4f}")
        context += f"\n[Chunk {chunk_id}]\n{chunk_text}\n"

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

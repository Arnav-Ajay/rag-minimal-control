# app.py → glue + debug prints

from llm import get_llm_response
from ingest import load_pdf, chunk_texts
from retriever import create_vector_store, retrieve_similar_documents

def main():

    query = "What is mentioned in this document?"

    pdf_path = r"data\ANNEXURE-E.pdf"
    text = load_pdf(pdf_path)

    chunks = chunk_texts(text)
    print(f"Total chunks created: {len(chunks)}")
    if len(chunks) == 1000:
        print("⚠️ Chunk limit reached. Document truncated for control-system execution.")


    vector_store = create_vector_store(chunks)

    top_k = 4
    results = retrieve_similar_documents(vector_store, query, top_k=top_k)
    print(f"Top {top_k} similar documents retrieved.")

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

# # ingest.py → PDF → chunks

from PyPDF2 import PdfReader

# Function to load PDF and extract text
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_texts(text, chunk_size=500, overlap=50, max_chunks=1000):
    chunks = {}
    start = 0
    text_length = len(text)
    chunk_id = 0

    while start < text_length and chunk_id < max_chunks:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks[chunk_id] = chunk
        chunk_id += 1
        start = end - overlap if overlap > 0 else end

    return chunks